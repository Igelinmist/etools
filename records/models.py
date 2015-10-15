from django.db import models

from .constans import EVENT_CHOICES, STATE_CHOICES
# from .constans import EXT_STATE_DATA, STANDARD_STATE_DATA, EVENT_CHOICES_DICT


class ProductionUnit(models.Model):
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
        ordering = ['plant_id', 'name']
        verbose_name = 'оборудование'
        verbose_name_plural = 'оборудование'

    def unit_tree(self):
        """
        Метод строит дерево (список) подчиненных объектов, включая отступ
        глубины.
        """
        def get_knot_dict(input_set):
            res = {}
            for unit in input_set:
                if unit.plant_id in res:
                    res[unit.plant_id].append(unit)
                else:
                    res[unit.plant_id] = [unit]
            return res

        def get_tree(knot_dict, tree, ident=0, node=None):
            if node:
                tree.append((node, ident))
            ident += 1
            for branch_object in knot_dict[node.id if node else None]:
                if branch_object.id in knot_dict:
                    get_tree(knot_dict, tree, ident, branch_object)
                else:
                    tree.append((branch_object, ident))

        units = ProductionUnit.objects.all()
        tree = []
        knot_dict = get_knot_dict(units)
        get_tree(knot_dict, tree, 0, self)
        return tree


class Journal(models.Model):
    """
    Модель Журнала записей статистики работы/простоя по конкретному
    оборудованию
    """

    equipment = models.OneToOneField(ProductionUnit, on_delete=models.CASCADE,
                                     related_name='journal')
    hot_rzv_stat = models.BooleanField(default=False)
    downtime_stat = models.BooleanField(default=False)
    stat_by_parent = models.BooleanField(default=False)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['equipment__name']
        verbose_name = 'журнал'
        verbose_name_plural = 'журналы'
        default_permissions = []
        permissions = (
            ('view_journal_details', 'Может просматривать записи журнала'),
            ('view_journal_list', 'Может посмотреть список журналов'),
            ('create_journal_record', 'Может создать запись в журнале'),
            ('edit_journal_record', 'Может редактировать запись в журнале'),
            ('delete_journal_record', 'Может удалить запись в журнале'),
            ('create_journal_event', 'Может создать событие в журнале'),
            ('delete_journal_event', 'Может удалить событие в журнале'),
        )

    def __str__(self):
        plant_name = self.equipment.plant.name if self.equipment.plant else '-'
        return plant_name + ' \ ' + self.equipment.name


class Record(models.Model):
    """
    Модель Одна строка стандартной записи журнала на дату начала периода
    """

    journal = models.ForeignKey('Journal', on_delete=models.CASCADE,
                                related_name='records')
    date = models.DateField()
    work = models.DurationField(default='0:00')
    pusk_cnt = models.IntegerField(default=0)
    ostanov_cnt = models.IntegerField(default=0)

    class Meta:
        unique_together = ('journal', 'date')
        default_permissions = []
        verbose_name = 'запись'
        verbose_name_plural = 'записи'

    def __str__(self):
        return "{0} | wt: {1} | pc: {2} | oc: {3}".format(
            self.date,
            self.work,
            self.pusk_cnt,
            self.ostanov_cnt)


class ExtStateItem(models.Model):
    """
    Модель расширения стандартной записи статистики дополнительным,
    ненулевым, временем нахождения в определенном типе простоя
    """

    record = models.ForeignKey('Record',
                               related_name='ext_states',
                               on_delete=models.CASCADE)
    state_code = models.CharField(max_length=3,
                                  choices=STATE_CHOICES,
                                  default='rsv',
                                  db_index=True)
    time_in_state = models.DurationField()

    class Meta:
        default_permissions = []


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
        default_permissions = []
