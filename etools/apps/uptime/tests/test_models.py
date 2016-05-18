from django.test import TestCase
from datetime import date, timedelta

from uptime.models.journal_models import Equipment, Journal
from uptime.models.report_models import Report


class JournalTestCase(TestCase):

    def setUp(self):
        eq = Equipment.objects.create(name='Test equipment')
        Journal.objects.create(equipment=eq, control_flags=253)

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

    def test_get_report_cell_simple(self):
        journal = Journal.objects.all()[0]
        journal.write_record('01.01.2015', wrk='15:00', arm='9:00', down_cnt=1)

        self.assertEquals(journal.get_report_cell(), '15')

    def test_get_report_cell_stat_from_kr(self):
        journal = Journal.objects.all()[0]
        journal.write_record('01.11.2014', wrk='24:00')
        journal.write_record('02.11.2014', krm='24:00', down_cnt=1)
        journal.write_record('01.01.2015', krm='24:00')
        journal.events.create(event_code='vkr', date='2015-01-02')
        journal.write_record('02.01.2015', wrk='15:00', krm='9:00', up_cnt=1)

        self.assertEquals(
            journal.get_report_cell(summary_type='ITV', from_event='FKR'),
            '15')
        self.assertEquals(
            journal.get_report_cell(summary_type='DT', from_event='FKR'),
            '02.01.2015')


class EquipmentTestCase(TestCase):

    fixtures = ['etools.json']

    def test_collect_sub_stat_on_date_still_no_data(self):
        """
        The journal_view function records_on_date
        Can call the Journal method collect_sub_stat_on_date (data for equipment tree)
        Get data for new date (empty data)
        """
        unit = Equipment.objects.get(pk=8)
        stat = unit.collect_sub_stat_on_date('01.03.2016')

        self.assertEquals(stat, [
            {'name': 'SubPlant_1', 'ident': 0},
            {'name': 'Eq-01',
             'journal_id': 1,
             'ident': 1,
             'has_data': False,
             'rec_data': {
                'rdate': '01.03.2016',
                'wrk': '0:00',
                'up_cnt': 0,
                'down_cnt': 0,
                'hrs': '0:00',
                'rsv': '0:00',
                'trm': '0:00',
                'arm': '0:00',
                'krm': '0:00',
                'srm': '0:00',
                'rcd': '0:00',
                'ksv': '0:00',
              }},
            {'name': 'Eq-02',
             'journal_id': 2,
             'ident': 1,
             'has_data': False,
             'rec_data': {
                'rdate': '01.03.2016',
                'wrk': '0:00',
                'up_cnt': 0,
                'down_cnt': 0,
                'hrs': '0:00',
                'rsv': '0:00',
                'trm': '0:00',
                'arm': '0:00',
                'krm': '0:00',
                'srm': '0:00',
                'rcd': '0:00',
                'ksv': '0:00',
             }}, ]
        )

    def test_collect_sub_stat_on_date_with_data(self):
        """
        The journal_view function records_on_date
        Can call the Journal method collect_sub_stat_on_date (data for equipment tree)
        Get data for date partly with data
        """
        unit = Equipment.objects.get(pk=8)
        stat = unit.collect_sub_stat_on_date('03.03.2016')

        self.assertEquals(stat, [
            {'name': 'SubPlant_1', 'ident': 0},
            {'name': 'Eq-01',
             'journal_id': 1,
             'ident': 1,
             'has_data': True,
             'rec_data': {
                'rdate': '03.03.2016',
                'wrk': '10:00',
                'up_cnt': 1,
                'down_cnt': 0,
                'hrs': '0:00',
                'rsv': '0:00',
                'trm': '0:00',
                'arm': '0:00',
                'krm': '0:00',
                'srm': '0:00',
                'rcd': '0:00',
                'ksv': '0:00',
              }},
            {'name': 'Eq-02',
             'journal_id': 2,
             'ident': 1,
             'has_data': False,
             'rec_data': {
                'rdate': '03.03.2016',
                'wrk': '0:00',
                'up_cnt': 0,
                'down_cnt': 0,
                'hrs': '0:00',
                'rsv': '0:00',
                'trm': '0:00',
                'arm': '0:00',
                'krm': '0:00',
                'srm': '0:00',
                'rcd': '0:00',
                'ksv': '0:00',
             }}, ]
        )


class ReportTestCase(TestCase):

    fixtures = ['etools.json']

    def test_prepare_report_data_no_events_no_time_limits(self):
        """
        The report_view function Show
        Can call the Report method 'prepare_report_data'
        Get data in output array with undefine date scope
        """
        rep = Report.objects.get(pk=1)

        self.assertEquals(
            rep.prepare_report_data(), [
                ['Оборудование', 'TW', 'Vv/Z', 'FrKR', 'VvKR', 'UpCnt'],
                ['Eq-01', '82', '-', '-', '-', '1'],
                ['Eq-02', '-', '-', '-', '-', '-']]
        )

    def test_prepare_report_data_no_events_with_low_time_limit(self):
        """
        The report_view function Show
        Can call the Report method 'prepare_report_data'
        Get data in output array in definite date scope (early time limit)
        """
        rep = Report.objects.get(pk=1)

        self.assertEquals(
            rep.prepare_report_data(report_date_from='2016-01-01'), [
                ['Оборудование', 'TW', 'Vv/Z', 'FrKR', 'VvKR', 'UpCnt'],
                ['Eq-01', '34', '-', '-', '-', '1'],
                ['Eq-02', '-', '-', '-', '-', '-']]
        )

    def test_prepare_report_data_no_events_with_high_time_limit(self):
        """
        The report_view function Show
        Can call the Report method 'prepare_report_data'
        Get data in output array in definite date scope (late time limit)
        """
        rep = Report.objects.get(pk=1)

        self.assertEquals(
            rep.prepare_report_data(report_date='2016-03-04'), [
                ['Оборудование', 'TW', 'Vv/Z', 'FrKR', 'VvKR', 'UpCnt'],
                ['Eq-01', '58', '-', '-', '-', '1'],
                ['Eq-02', '-', '-', '-', '-', '-']]
        )

    def test_prepare_report_data_no_events_with_time_limits(self):
        """
        The report_view function Show
        Can call the Report method 'prepare_report_data'
        Get data in output array in definite date scope (both side limit)
        """
        rep = Report.objects.get(pk=1)

        self.assertEquals(
            rep.prepare_report_data(report_date='2016-03-04', report_date_from='2016-03-03'), [
                ['Оборудование', 'TW', 'Vv/Z', 'FrKR', 'VvKR', 'UpCnt'],
                ['Eq-01', '10', '-', '-', '-', '-'],
                ['Eq-02', '-', '-', '-', '-', '-']]
        )

    def test_prepare_report_data_with_event_zamena_no_time_limits(self):
        """
        The report_view function Show
        Can call the Report method 'prepare_report_data'
        Get data about Zamena and Utime after it in output array
        """
        rep = Report.objects.get(pk=1)
        journal = Journal.objects.get(pk=1)
        journal.events.create(event_code='zmn', date='2016-01-01')

        self.assertEquals(
            rep.prepare_report_data(), [
                ['Оборудование', 'TW', 'Vv/Z', 'FrKR', 'VvKR', 'UpCnt'],
                ['Eq-01', '34', '01.01.2016', '-', '-', '1'],
                ['Eq-02', '-', '-', '-', '-', '-']]
        )

    def test_prepare_report_data_with_event_vvod_kr_no_time_limits(self):
        """
        The report_view function Show
        Can call the Report method 'prepare_report_data'
        Get data about KR and Uptime after it in output array
        """
        rep = Report.objects.get(pk=1)
        journal = Journal.objects.get(pk=1)
        journal.events.create(event_code='vkr', date='2016-03-02')

        self.assertEquals(
            rep.prepare_report_data(), [
                ['Оборудование', 'TW', 'Vv/Z', 'FrKR', 'VvKR', 'UpCnt'],
                ['Eq-01', '82', '-', '34', '02.03.2016', '1'],
                ['Eq-02', '-', '-', '-', '-', '-']]
        )

    def test_prepare_report_data_including_hot_reserv(self):
        """
        The report_view function Show
        Can call the Report method 'prepare_report_data'
        Get data in output array with undefine date scope and hot reserv stat
        """
        rep = Report.objects.get(pk=2)

        self.assertEquals(
            rep.prepare_report_data(), [
                ['Оборудование', 'TW'],
                ['Eq_hr-01', '48']]
        )
