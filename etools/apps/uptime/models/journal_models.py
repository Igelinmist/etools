from datetime import timedelta, datetime, date
from django.db import models

from ..constants import EVENT_CHOICES, STATE_CHOICES
from ..constants import RECORD_SET, INTERVAL_SET, B_FORM, DS_FORM, HR_FORM
from ..utils import req_date, stat_timedelta_for_report
from ..forms.journal_forms import BaseRecordForm, DownStatRecordForm, HotReservRecordForm


class EquipmentManager(models.Manager):

    def get_queryset(self):
        return super(EquipmentManager, self).get_queryset().select_related('journal')


class Equipment(models.Model):

    """
    Модель производственных единиц от Предприятия до Детали Оборудования
    """
    plant = models.ForeignKey('self', blank=True, null=True,
                              related_name='parts', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

    def __str__(self):
        if self.plant is None:
            plant_name = '\\'
        else:
            plant_name = self.plant
        return '{0} - {1}'.format(plant_name, self.name)

    class Meta:
        db_table = 'equipment'
        ordering = ['plant_id', 'name']
        verbose_name = 'оборудование'
        verbose_name_plural = 'оборудование'

    objects = EquipmentManager()

    @property
    def journal_id(self):
        if '_journal_cache' in self.__dict__:
            if self._journal_cache:
                return self._journal_cache.id
            else:
                return None
        else:
            return None

    def unit_tree(self):
        """
        Description: Метод строит дерево (список) подчиненных объектов, включая отступ
        глубины вложенности.
        """
        def get_knot_dict(units):
            res = {}
            for unit in units:
                if unit.plant_id in res:
                    res[unit.plant_id].append(unit)
                else:
                    res[unit.plant_id] = [unit]
            return res

        def get_tree(knot_dict, tree, ident=0, node=None):
            if node:
                tree.append((node, ident))
            ident += 1
            for eq in knot_dict[node.id if node else None]:
                if eq.id in knot_dict:
                    get_tree(knot_dict, tree, ident, eq)
                else:
                    tree.append((eq, ident))

        units = Equipment.objects.all()
        tree = []
        knot_dict = get_knot_dict(units)
        get_tree(knot_dict, tree, 0, self)
        return tree

    def collect_sub_stat_on_date(self, stat_date):
        """
        Description: Метод собирает все наличествующие записи статистики для дерева
        журналов (на базе дерева оборудования).
        """
        eq_list = self.unit_tree()
        # Собрать все номера журналов
        journal_set = {
            eq.journal_id for eq, ident in eq_list
            if eq.journal_id and not eq.journal.stat_by_parent
        }
        # для запроса существующих записей на дату
        records = Record.objects.filter(rdate=req_date(stat_date), journal_id__in=journal_set).all()
        journals_records = {rec.journal_id: rec for rec in records}
        res = []
        for eq, ident in eq_list:
            row = {}
            if eq.journal_id and not eq.journal.stat_by_parent:
                row['name'] = eq.name
                row['journal_id'] = eq.journal_id
                row['ident'] = ident
                row['form_type'] = B_FORM
                if eq.journal.downtime_stat:
                    row['form_type'] = row['form_type'] | DS_FORM
                if eq.journal.hot_rzv_stat:
                    row['form_type'] = row['form_type'] | HR_FORM
                if eq.journal_id in journals_records:
                    row['rec_data'] = journals_records[eq.journal_id].data_dict()
                    row['has_record'] = True
                else:
                    row['rec_data'] = {'rdate': stat_date, 'up_cnt': 0, 'down_cnt': 0}
                    for state in INTERVAL_SET:
                        row['rec_data'][state] = '0:00'
                    row['has_record'] = False
                res.append(row)
            elif not eq.journal_id:
                row['name'] = eq.name
                row['ident'] = ident
                row['form_type'] = 0
                res.append(row)
        return res


class JournalManager(models.Manager):

    def get_queryset(self):
        return super(JournalManager, self).get_queryset().select_related()


class Journal(models.Model):

    """
    Модель Журнала записей статистики работы/простоя по конкретному
    оборудованию
    """

    equipment = models.OneToOneField(Equipment, on_delete=models.CASCADE,
                                     related_name='journal')
    stat_by_parent = models.BooleanField(default=False)
    hot_rzv_stat = models.BooleanField(default=False)
    downtime_stat = models.BooleanField(default=False)
    description = models.TextField(blank=True)

    objects = JournalManager()
    journal = JournalManager()

    class Meta:
        db_table = 'journals'
        ordering = ['equipment__name']
        verbose_name = 'журнал'
        verbose_name_plural = 'журналы'
        default_permissions = []
        permissions = (
            ('view_journal_details', 'View journal details'),
            ('view_journal_list', 'View journal list'),
            ('create_journal_record', 'Create record'),
            ('edit_journal_record', 'Edit record'),
            ('delete_journal_record', 'Delete record'),
            ('create_journal_event', 'Create journal event'),
            ('delete_journal_event', 'Delete journal event'),
        )

    def __str__(self):
        plant_name = self._equipment_cache.plant.name if self._equipment_cache.plant else '-'
        return plant_name + ' \ ' + self._equipment_cache.name

    def write_record(self, rdate, **rdata):
        """
        Description: Метод создает новую запись (или обновляет существующую)
        на основе входного словаря.
        """
        # Разделяем словарь входных данных на то, что относится к записи
        # и то, что к интревалам
        rec_keys = rdata.keys() & RECORD_SET
        interval_keys = rdata.keys() & INTERVAL_SET
        rec_argv = {key: rdata[key] for key in rec_keys}
        # Пробуем найти запись на эту дату
        try:
            rec = self.records.filter(rdate=req_date(rdate))[0]
            # Проверяем изменение данных записи
            changed_fields = []
            for name in rec_keys:
                if rec.__getattribute__(name) != rec_argv[name]:
                    changed_fields.append(name)
                    rec.__setattr__(name, rec_argv[name])
            rec.save(update_fields=changed_fields)
            # Изменяем (удаляем -> создаем) интервалы
            rec.intervals.all().delete()
            for key in interval_keys:
                rec.__setattr__(key, rdata[key])

        except IndexError:
            rec = self.records.create(rdate=req_date(rdate), **rec_argv)
            for key in interval_keys:
                rec.__setattr__(key, rdata[key])
        return rec

    def get_last_records(self, depth=10):
        """
        Description: Метод возвращает выборку последних записей на нужную глубину.
        """
        if self.stat_by_parent:
            return self.equipment.plant.journal.get_last_records(depth)
        else:
            return self.records.order_by('-rdate')[:depth]

    def switch_date_get_rec(self, curent_date_local, offset_str):
        """
        Description: Метод переключает дату от заданной на нужное смещение
        и возвращает запись на новую дату при наличии.
        """
        cur_date = datetime.strptime(curent_date_local, '%d.%m.%Y')
        new_date = cur_date + timedelta(int(offset_str))
        rset = self.records.filter(rdate=new_date.strftime("%Y-%m-%d"))
        if rset.exists():
            return rset[0], new_date.strftime("%d.%m.%Y")
        else:
            return None, new_date.strftime("%d.%m.%Y")

    def delete_record(self, record_id):
        """
        Description: Метод удаляет существующую запись статистики.
        """
        rec = self.records.get(pk=record_id)
        rec.delete()

    def get_record_data(self, record_id):
        """
        Description: Метод получения данных для инициализации полей формы
        существующей записью
        """
        rec = self.records.get(pk=record_id)
        return rec.data_dict()

    def set_event_data(self, data):
        self.events.create(
            date=data['date'],
            event_code=data['event_code'])

    # Методы для формирования отчетов

    def get_stat(self, from_date=None, to_date=None, state_code='wrk'):
        """
        Description: Метод расчет суммарного времени нахождения в некотором состоянии
        (по умолчанию в работе) на временном интервале
        """
        r_set = self.records
        if from_date:
            r_set = r_set.filter(rdate__gte=from_date)
        if to_date:
            r_set = r_set.exclude(rdate__gte=to_date)
        r_set = r_set.filter(intervals__state_code=state_code)
        total = r_set.aggregate(models.Sum('intervals__time_in_state'))['intervals__time_in_state__sum']
        return stat_timedelta_for_report(total)

    def get_journal_or_subjournal(self, part_name=None):
        if part_name:
            eq = self.equipment
            try:
                part = eq.parts.filter(name=part_name)[0]
                return part.journal if part.journal else None
            except IndexError:
                return None
        else:
            return self

    def get_report_cell(self, summary_type='ITV', from_event='FVZ', date_to=None, date_from=None):
        from_event_to_event_dict = {
            'FVZ': 'zmn',
            'FKR': 'vkr',
            'FSR': 'vsr',
            'FRC': 'vrc',
        }
        journal = self.equipment.plant.journal if self.stat_by_parent else self
        rec_set = journal.records  # Начитаем готовить query_set здесь он еще не выполняется
        try:
            date_from_event = self.events.filter(
                event_code=from_event_to_event_dict[from_event]
            ).order_by('-date')[0].date
            if summary_type == 'DT':
                return date_from_event.strftime("%d.%m.%Y")
        except IndexError:
            date_from_event = None
            if from_event != 'FVZ':
                return '-'
            elif summary_type == 'DT':
                return '-'
        if date_from_event:
            # Время "от события" откатываем на начало месяца, поскольку
            # капитальный и средный ремонты, замены и реконструкции
            # длятся не менее месяца, а раньше интервалы фиксировались
            # за месяц или год, что приводит к неверному расчету
            date_from_event = date(date_from_event.year, date_from_event.month, 1)
        # Теперь нужно выбрать дату от которой плясать
        # Если задано время начала отчета и было вычислено время "от события" - надо выбрать одно из двух
        if date_from and date_from_event:
            y, m, d = date_from.split('-')
            date_from = date_from if date(int(y), int(m), int(d)) > date_from_event else date_from_event
            rec_set = rec_set.filter(rdate__gt=date_from)
        elif date_from:
            # Если задано время начала отчета, но нет времени события - использовать его как начало
            rec_set = rec_set.filter(rdate__gt=date_from)
        elif date_from_event:
            date_from = date_from_event
            rec_set = rec_set.filter(rdate__gt=date_from)

        # Если не задано ни то ни другое время - считаем все записи, предшествующие времени, т.е. не используем условие

        if date_to:
            rec_set = rec_set.exclude(rdate__gte=date_to)
        else:
            rec_set = rec_set.exclude(rdate__gte=date.today())
        if summary_type == 'PCN':
            return rec_set.aggregate(models.Sum('up_cnt'))['up_cnt__sum']
        elif summary_type == 'OCN':
            return rec_set.aggregate(
                models.Sum('down_cnt'))['down_cnt__sum']
        else:
            return journal.get_stat(
                from_date=date_from,
                to_date=date_to,
                state_code='wrk'
            )

    @property
    def is_deregister(self):
        ev = self.events.order_by('-date').all()
        if ev and ev[0].event_code == 'sps':
            return True
        else:
            return False

    def recordFormClass(self):
        if self.downtime_stat:
            return DownStatRecordForm
        elif self.hot_rzv_stat:
            return HotReservRecordForm
        else:
            return BaseRecordForm


class RecordManager(models.Manager):

    def get_queryset(self):
        return super(RecordManager, self).get_queryset().prefetch_related('intervals')


class Record(models.Model):

    journal = models.ForeignKey('Journal', on_delete=models.CASCADE,
                                related_name='records')
    rdate = models.DateField()
    up_cnt = models.IntegerField(default=0)
    down_cnt = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    records = RecordManager()
    objects = RecordManager()

    class Meta:
        db_table = 'records'
        # unique_together = ('journal', 'rdate')

    class StateDescriptor:

        def __init__(self, state_code):
            self.state_code = state_code

        def __get__(self, instance, owner):
            try:
                for interval in instance._prefetched_objects_cache['intervals']:
                    if interval.state_code == self.state_code:
                        return interval.stat_time
            except (AttributeError, KeyError):
                q_set = instance.intervals.filter(state_code=self.state_code)
                if q_set.exists():
                    return q_set[0].stat_time
                else:
                    return '0:00'
            return '0:00'

        def __set__(self, instance, value):
            if isinstance(value, str):
                try:
                    hr, mnt = value.split(':')
                    interval = timedelta(hours=int(hr), minutes=int(mnt))
                except ValueError:
                    return 'Bad value for timedelta'
            elif isinstance(value, timedelta):
                interval = value
            else:
                return 'Bad value for timedelta'
            if interval != timedelta(0):
                instance.intervals.create(state_code=self.state_code, time_in_state=interval)

    wrk = StateDescriptor('wrk')
    hrs = StateDescriptor('hrs')
    rsv = StateDescriptor('rsv')
    trm = StateDescriptor('trm')
    arm = StateDescriptor('arm')
    krm = StateDescriptor('krm')
    srm = StateDescriptor('srm')
    rcd = StateDescriptor('rcd')

    def data_dict(self):
        """
        Description: Метод получения данных для инициализации полей формы
        существующей записью
        """
        data = {}
        data['rdate'] = self.rdate.strftime('%d.%m.%Y')
        data['up_cnt'] = self.up_cnt
        data['down_cnt'] = self.down_cnt
        for state in INTERVAL_SET:
            data[state] = self.__getattribute__(state)
        return data


class IntervalItem(models.Model):

    record = models.ForeignKey('Record',
                               related_name='intervals',
                               on_delete=models.CASCADE)
    state_code = models.CharField(max_length=3,
                                  choices=STATE_CHOICES,
                                  default='wrk',
                                  db_index=True)
    time_in_state = models.DurationField()

    class Meta:
        db_table = 'intervals'
        default_permissions = []

    def __str__(self):
        return '%s>%s' % (self.state_code, self.stat_time)

    @property
    def stat_time(self):
        sec = self.time_in_state.total_seconds()
        hours, remainder = divmod(sec, 3600)
        minutes, sec = divmod(remainder, 60)
        return '%d:%02d' % (int(hours), int(minutes))


class EventItem(models.Model):

    """
    Модель Отражение события жизненного цикла
    из предопределенного набора: [Ввод, Списание, Замена]
    """

    journal = models.ForeignKey('Journal',
                                related_name='events',
                                on_delete=models.CASCADE)
    date = models.DateField()
    event_code = models.CharField(max_length=3,
                                  choices=EVENT_CHOICES)

    class Meta:
        db_table = 'event_items'
        default_permissions = []
