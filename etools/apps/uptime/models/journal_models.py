from datetime import timedelta, datetime

from django.db import models

from ..constants import EVENT_CHOICES, STATE_CHOICES
from ..constants import RECORD_SET, INTERVAL_SET
from ..utils import req_date, req_timedelta


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

    def journal_id(self):
        try:
            return self.journal.id
        except Journal.DoesNotExist:
            return None

    def unit_tree(self):
        """
        Метод строит дерево (список) подчиненных объектов, включая отступ
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
                    tree.append((dict(id=eq.id,
                                      name=eq.name,
                                      journal_id=eq.journal_id),
                                 ident))

        units = Equipment.objects.select_related().all()
        tree = []
        knot_dict = get_knot_dict(units)
        get_tree(knot_dict, tree, 0, self)
        return tree


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
        # Разделяем словарь входных данных на то, что относится к записи
        # и то, что к интревалам
        rec_keys = rdata.keys() & RECORD_SET
        interval_keys = rdata.keys() & INTERVAL_SET
        rec_argv = {key: rdata[key] for key in rec_keys}
        intervals_argv = {key: rdata[key] for key in interval_keys}
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
            rec.set_intervals(intervals_argv)
        except IndexError:
            rec = self.records.create(rdate=req_date(rdate), **rec_argv)
            rec.set_intervals(intervals_argv)
        return rec

    def get_last_records(self, depth=10):
        if self.stat_by_parent:
            return self.equipment.plant.journal.get_last_records(depth)
        else:
            return self.records.order_by('-rdate')[:depth]

    def switch_date_get_rec(self, curent_date_local, offset_str):
        cur_date = datetime.strptime(curent_date_local, '%d.%m.%Y')
        new_date = cur_date + timedelta(int(offset_str))
        rset = self.records.filter(rdate=new_date.strftime("%Y-%m-%d"))
        if rset.exists():
            return rset[0], new_date.strftime("%d.%m.%Y")
        else:
            return None, new_date.strftime("%d.%m.%Y")


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

    def _in_state(self, state_name):
        try:
            for interval in self._prefetched_objects_cache['intervals']:
                if interval.stat_code == state_name:
                    return interval.stat_time
        except (AttributeError, KeyError):
            print(self.__dict__)
            q_set = self.intervals.filter(state_code=state_name)
            if q_set.exists():
                return q_set[0].stat_time
            else:
                return '0:00'
        return '0:00'

    @property
    def wrk(self):
        return self._in_state('wrk')

    @property
    def hrs(self):
        return self._in_state('hrs')

    @property
    def rsv(self):
        return self._in_state('rsv')

    @property
    def trm(self):
        return self._in_state('trm')

    @property
    def arm(self):
        return self._in_state('arm')

    @property
    def krm(self):
        return self._in_state('krm')

    @property
    def srm(self):
        return self._in_state('srm')

    @property
    def rcd(self):
        return self._in_state('rcd')

    def set_intervals(self, i_dict):
        for interval in i_dict:
            t_i_s = req_timedelta(i_dict[interval])
            if t_i_s:
                self.intervals.create(state_code=interval,
                                      time_in_state=t_i_s)


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
