from django.db import models

from .journal_models import Equipment, Journal


class Report(models.Model):
    """
    Модель Отчета для определенной группы оборудования. Каждый отчет относится
    к группе оборудования, но не каждое оборудование имеет отчет.
    """

    equipment = models.OneToOneField(
        Equipment, related_name='report', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    is_generalizing = models.BooleanField(default=False)
    weight = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'отчет'
        verbose_name_plural = 'отчеты'
        default_permissions = []
        db_table = 'reports'

    def prepare_journals_id_for_report(self):
        """
        Подготовка промежуточной таблицы для формирования отчета.
        В ячейках вместо данных содержится id журнала, из которого необходимо
        обработать данные.
        """
        columns = self.columns.order_by('weight').all()
        part_set = self.equipment.parts.order_by('name').all()
        journals_id_table = []
        for part in part_set:
            journals_id_table.append([
                part.journal.get_journal_or_subjournal_id(
                    col.element_name_filter
                )
                for col in columns
            ])
        return {
            'journals_id': journals_id_table,
            'columns': columns,
            'parts': part_set
        }

    def prepare_report_data(self, report_date=None):
        """
        Метод заполняет данными таблицу для отчета
        """
        report_data = self.prepare_journals_id_for_report()
        journals_id = report_data['journals_id']
        columns = report_data['columns']
        part_set = report_data['parts']
        report_table = [
            [subunit.name] + [
                Journal.objects.get(
                    pk=journals_id[indxr][indxc]
                ).get_report_cell(
                    from_event=col.from_event,
                    summary_type=col.column_type,
                    date_to=report_date
                ) if journals_id[indxr][indxc] else '-'
                for (indxc, col) in enumerate(columns)
            ]
            for (indxr, subunit) in enumerate(part_set)
        ]
        titles = ['Оборудование'] + [col.title for col in columns]
        report_table = [titles] + report_table
        return report_table

    def get_reports_collection(root_eq):
        """
        Description: Метод готовит коллекцию отчетов для дерева
        оборудования.
        """

        def eq_has_report(equipment):
            try:
                if equipment.report:
                    return True
            except Report.DoesNotExist:
                return False

        report_set = []
        equipment_tree = root_eq.unit_tree()
        for eq, ident in equipment_tree:
            if eq_has_report(eq):
                report_set.append(
                    (eq.report.id, '--' * ident + eq.report.title)
                )
        return report_set

    def prepare_reports_content(self, ru_date=None):
        """
        Метод готовит одну или несколько таблиц отчетов,
        в зависимости от того, является ли исходный отчет
        обобщающим. Предполагается, что дата поступает
        в российском формате, надо ее переводить в формат,
        который переваривает django запрос.
        """
        if ru_date:
            d, m, y = ru_date.split('.')
            qdate = '{}-{}-{}'.format(y, m, d)
        else:
            qdate = None
        report_list = []
        if self.is_generalizing:
            for eq in self.equipment.parts.order_by('name').all():
                try:
                    temp_report = eq.report
                    temp_report_table = temp_report.prepare_report_data(
                        report_date=qdate
                    )
                    report_list.append((temp_report, temp_report_table))
                except Report.DoesNotExist:
                    continue
        else:
            report_list.append(
                (self,
                 self.prepare_report_data(report_date=qdate))
            )
        return report_list


TYPE_CHOICES = (
    ('ITV', 'Интервал'),
    ('DT', 'Дата'),
    ('PCN', 'Количество пусков'),
    ('OCN', 'Количество остановов'),
)

FROM_EVENT_CHOICES = (
    ('FVZ', 'ввод/замена'),
    ('FKR', 'капремонт'),
    ('FSR', 'средний ремонт'),
    ('FRC', 'реконструкция'),
)


class Column(models.Model):
    """
    Модель конфигурации столбца отчета
    """

    report = models.ForeignKey(
        Report,
        related_name='columns',
        on_delete=models.CASCADE,
    )
    title = models.CharField(max_length=128)
    column_type = models.CharField(max_length=3,
                                   choices=TYPE_CHOICES)
    from_event = models.CharField(max_length=3,
                                  choices=FROM_EVENT_CHOICES)
    element_name_filter = models.CharField(max_length=50,
                                           blank=True)
    weight = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'столбец'
        verbose_name_plural = 'столбцы'
        ordering = ['weight']
        default_permissions = []
        db_table = 'columns'
