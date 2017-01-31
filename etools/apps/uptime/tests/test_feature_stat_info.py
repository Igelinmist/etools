from django.test import TestCase

from uptime.models.journal_models import Journal


class FeatureStatInfoTestCase(TestCase):

    fixtures = ['some_stat.json']

    def test_get_state_stat_dict_for_report(self):
        journal = Journal.objects.get(pk=1)

        self.assertEquals(journal.state_stat(), {
            'arm': '9',
            'krm': '22',
            'rcd': '-',
            'rsv': '-',
            'srm': '-',
            'trm': '-',
            'wrk': '41'})

    def test_get_state_stat_dict_for_journal_page(self):
        journal = Journal.objects.get(pk=1)

        self.assertEquals(journal.state_stat(round_to_hour=False), {
            'arm': '9:29',
            'krm': '21:32',
            'rcd': '-',
            'rsv': '-',
            'srm': '-',
            'trm': '-',
            'wrk': '40:59'})

    def test_get_full_stat_dict_for_journal_page(self):
        journal = Journal.objects.get(pk=1)

        self.assertEquals(journal.full_stat(), {
            'arm': '9:29',
            'down_cnt': 1,
            'krm': '21:32',
            'rcd': '-',
            'rsv': '-',
            'srm': '-',
            'trm': '-',
            'up_cnt': 1,
            'wrk': '40:59'})
