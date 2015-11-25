from django.test import TestCase
from datetime import date, timedelta

from ..models.journal_models import Equipment, Journal
from ..models.report_models import Report, Column
from ..constants import B_FORM, DS_FORM


class JournalTestCase(TestCase):

    def setUp(self):
        eq = Equipment.objects.create(name='Test equipment')
        Journal.objects.create(equipment=eq, downtime_stat=True)

    def test_journal_can_add_record(self):
        journal = Journal.objects.all()[0]
        journal.write_record('01.01.2015', wrk='15:00', arm='9:00', down_cnt=1)
        rec = journal.records.filter(rdate='2015-01-01').all()[0]

        self.assertEquals(rec.rdate.strftime('%d.%m.%Y'), '01.01.2015')
        self.assertEquals(rec.wrk, '15:00')
        self.assertEquals(rec.arm, '9:00')
        self.assertEquals(rec.trm, '0:00')

    def test_journal_can_change_record(self):
        journal = Journal.objects.all()[0]
        journal.write_record('01.01.2015', wrk='15:00', arm='9:00', down_cnt=1)
        journal.write_record('01.01.2015', wrk='14:00',
                             arm='10:00', down_cnt=2, up_cnt=1)
        rset = journal.records.filter(rdate='2015-01-01')
        cnt = rset.count()
        rec = rset.all()[0]

        self.assertEquals(cnt, 1)
        self.assertEquals(rec.rdate.strftime('%d.%m.%Y'), '01.01.2015')
        self.assertEquals(rec.wrk, '14:00')
        self.assertEquals(rec.arm, '10:00')
        self.assertEquals(rec.trm, '0:00')
        self.assertEquals(rec.down_cnt, 2)
        self.assertEquals(rec.up_cnt, 1)

    def test_journal_get_last_record_list(self):
        journal = Journal.objects.all()[0]
        for offset in range(5):
            dt = (date(2015, 1, 1) + timedelta(days=offset)).strftime("%d.%m.%Y")
            journal.write_record(dt, wrk='24:00')
        date_list = [rec.rdate for rec in journal.get_last_records(depth=3)]

        self.assertEquals(date_list, [date(2015, 1, 5),
                                      date(2015, 1, 4),
                                      date(2015, 1, 3), ])

    def test_journal_get_last_record_list_for_child(self):
        journal = Journal.objects.all()[0]
        child_equipment = journal.equipment.parts.create()
        child_journal = Journal(equipment=child_equipment, stat_by_parent=True)
        child_journal.save()
        # Добавляем записей для журнала родительского оборудования
        for offset in range(5):
            dt = (date(2015, 1, 1) + timedelta(days=offset)).strftime("%d.%m.%Y")
            journal.write_record(dt, wrk='24:00')
        date_list_child = [rec.rdate for rec in child_journal.get_last_records(depth=3)]

        self.assertEquals(date_list_child, [date(2015, 1, 5),
                                            date(2015, 1, 4),
                                            date(2015, 1, 3), ])

    def test_journal_switch_record_on_exist_record(self):
        journal = Journal.objects.all()[0]
        journal.write_record('01.01.2015', wrk='15:00', arm='9:00', down_cnt=1)
        rec, rdate = journal.switch_date_get_rec('02.01.2015', '-1')

        self.assertEquals(rdate, '01.01.2015')
        self.assertEquals(rec.wrk, '15:00')

    def test_journal_switch_record_on_nonexist_record(self):
        journal = Journal.objects.all()[0]
        journal.write_record('01.01.2015', wrk='15:00', arm='9:00', down_cnt=1)
        rec, rdate = journal.switch_date_get_rec('02.01.2015', '+1')

        self.assertEquals(rdate, '03.01.2015')
        self.assertEquals(rec, None)

    def test_get_stat(self):
        journal = Journal.objects.all()[0]
        journal.write_record('01.01.2015', wrk='15:00', arm='9:00', down_cnt=1)

        self.assertEquals(journal.get_stat(state_code='wrk'), '15')
        self.assertEquals(journal.get_stat(state_code='arm'), '9')


class EquipmentTestCase(TestCase):

    def setUp(self):
        gr = Equipment.objects.create(name='Group')
        mu = Equipment.objects.create(name='Main Unit', plant=gr)
        su = Equipment.objects.create(name='Sub Unit', plant=mu)
        journal = Journal.objects.create(equipment=mu, downtime_stat=True)
        journal.write_record('01.01.2015', wrk='15:00', arm='9:00', down_cnt=1)
        Journal.objects.create(equipment=su, stat_by_parent=True)

    def test_collect_sub_stat_on_date_all_empty(self):
        head_unit = Equipment.objects.filter(plant=None)[0]
        sub_stat = head_unit.collect_sub_stat_on_date('02.01.2015')
        journal = Journal.objects.all()[0]

        self.assertEquals(sub_stat,
                          [{'name': 'Group', 'ident': 0, 'form_type': 0},
                           {'name': 'Main Unit',
                            'journal_id': journal.id,
                            'ident': 1, 'form_type': B_FORM | DS_FORM,
                            'rec_data': {'rdate': '02.01.2015',
                                         'wrk': '0:00',
                                         'up_cnt': 0,
                                         'down_cnt': 0,
                                         'rsv': '0:00',
                                         'trm': '0:00',
                                         'arm': '0:00',
                                         'krm': '0:00',
                                         'srm': '0:00',
                                         'rcd': '0:00',
                                         }}])

    def test_collect_sub_stat_on_date_has_record(self):
        head_unit = Equipment.objects.filter(plant=None)[0]
        sub_stat = head_unit.collect_sub_stat_on_date('01.01.2015')
        journal = Journal.objects.all()[0]

        self.assertEquals(sub_stat,
                          [{'name': 'Group', 'ident': 0, 'form_type': 0},
                           {'name': 'Main Unit',
                            'journal_id': journal.id,
                            'ident': 1, 'form_type': B_FORM | DS_FORM,
                            'rec_data': {'rdate': '01.01.2015',
                                         'wrk': '15:00',
                                         'up_cnt': 0,
                                         'down_cnt': 1,
                                         'rsv': '0:00',
                                         'trm': '0:00',
                                         'arm': '9:00',
                                         'krm': '0:00',
                                         'srm': '0:00',
                                         'rcd': '0:00',
                                         }}])


# class ReportTestCase(TestCase):

#     def setUp(self):
#         eobj = Equipment.objects.create(name='EObject')
#         gr = Equipment.objects.create(name='Group')
#         mu = Equipment.objects.create(name='Unit', plant=gr)
#         su = Equipment.objects.create(name='SubUnit', plant=mu)
#         journal = Journal.objects.create(equipment=mu, downtime_stat=True)
#         journal.write_record('01.11.2014', wrk='24:00')
#         journal.write_record('02.11.2014', krm='24:00', down_cnt=1)
#         journal.write_record('01.01.2015', krm='24:00')
#         journal.events.create(event_code='vkr', date='2015-01-02')
#         journal.write_record('02.01.2015', wrk='15:00', krm='9:00', up_cnt=1)
#         Journal.objects.create(equipment=su, stat_by_parent=True)
#         Report.objects.create(equipment=eobj, is_generalizing=True, title='Report Name')
#         rep = Report.objects.create(equipment=gr, title='Units')
#         rep.columns.create(title='TotalWork', column_type='ITV', from_event='FVZ')
#         rep.columns.create(title='Vvod/Zamena', column_type='DT', from_event='FVZ', weight=1)
#         rep.columns.create(title='FromKR', column_type='ITV', from_event='FKR', weight=2)
#         rep.columns.create(title='VvodKR', column_type='DT', from_event='FKR', weight=3)
#         rep.columns.create(title='TotalWorkSubunit', column_type='ITV',
#                            from_event='FVZ', weight=4, element_name_filter='SubUnit')
#         rep.columns.create(title='ZamenaSubunit', column_type='DT',
#                            from_event='FVZ', weight=5, element_name_filter='SubUnit')
#         rep.columns.create(title='UpCnt', column_type='PCN', from_event='FVZ', weight=6)
#         rep.columns.create(title='DownCnt', column_type='OCN', from_event='FVZ', weight=7)

#     def test_prepare_journals_id_for_report(self):
#         rep = Report.objects.filter(title='Units')[0]
#         eq_set = Equipment.objects
#         j = eq_set.filter(name='Unit')[0].journal.id
#         sj = eq_set.filter(name='SubUnit')[0].journal.id

#         self.assertEquals(rep.prepare_journals_id_for_report()['journals_id'],
#                           [[j, j, j, j, sj, sj, j, j]])
