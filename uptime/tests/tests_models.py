from django.test import TestCase

from uptime.models import Equipment, Journal, Record, IntervalItem


class JournalTestCase(TestCase):
    def setUp(self):
        eq = Equipment.objects.create(name='Test equipment')
        Journal.objects.create(equipment=eq, downtime_stat=True)

    def test_journal_can_add_record(self):
        journal = Journal.objects.all()[0]
        journal.write_record('01.01.2015', wrk='15:00', arm='9:00', down_cnt=1)
        rec = journal.records.filter(rdate='2015-01-01').all()[0]

        self.assertEquals(rec.rdate, '01.01.2015')
        self.assertEquals(rec.wrk, '15:00')
        self.assertEquals(rec.arm, '9:00')
