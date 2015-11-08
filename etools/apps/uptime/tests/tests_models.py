from django.test import TestCase
from datetime import date, timedelta

from uptime.models.journal_models import Equipment, Journal


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
        rec, rdate = journal.switch_rec('02.01.2015', '-1')

        self.assertEquals(rdate, '01.01.2015')
        self.assertEquals(rec.wrk, '15:00')

    def test_journal_switch_record_on_nonexist_record(self):
        journal = Journal.objects.all()[0]
        journal.write_record('01.01.2015', wrk='15:00', arm='9:00', down_cnt=1)
        rec, rdate = journal.switch_rec('02.01.2015', '+1')

        self.assertEquals(rdate, '03.01.2015')
        self.assertEquals(rec, None)
