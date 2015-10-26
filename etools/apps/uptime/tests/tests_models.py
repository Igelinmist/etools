from django.test import TestCase

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
