from datetime import timedelta, datetime

from django.db import models

from ..constants import EVENT_CHOICES, STATE_CHOICES
from ..constants import RECORD_SET, INTERVAL_SET, B_FORM, DS_FORM, HR_FORM
from ..utils import req_date


class EquipmentManager(models.Manager):

    def get_queryset(self):
        return super(EquipmentManager, self).get_queryset().select_related()


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

    @property
    def journal_id(self):
        try:
            return self.journal.id
        except Journal.DoesNotExist:
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
                else:
                    row['rec_data'] = {'rdate': stat_date, 'up_cnt': 0, 'down_cnt': 0}
                    for state in INTERVAL_SET:
                        row['rec_data'][state] = '0:00'
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
        plant_name = self.equipment.plant.name if self.equipment.plant else '-'
        return plant_name + ' \ ' + self.equipment.name

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
        unique_together = ('journal', 'rdate')

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
