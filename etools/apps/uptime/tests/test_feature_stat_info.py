from django.test import TestCase

from uptime.models.journal_models import Journal


class FeatureStatInfoTestCase(TestCase):

    fixtures = ['some_stat.json']

    def test_get_state_stat_dict_for_report(self):
        """
        Проверка подготовки данных для отчета:
        - Статистика запрашивается по умолчанию вся;
        - Статистика округляется до часа
        """
        journal = Journal.objects.get(pk=1)

        self.assertEquals(journal.state_stat(), {
            'arm': '9',
            'krm': '22',
            'rcd': '48',
            'rsv': '11',
            'srm': '-',
            'trm': '-',
            'wrk': '54'})

    def test_get_state_stat_dict_for_journal_page(self):
        """
        Проверка подготовки данных для страницы журнала:
        - Статистика запрашивается по умолчанию вся;
        - Статистика не округляется
        """
        journal = Journal.objects.get(pk=1)

        self.assertEquals(journal.state_stat(round_to_hour=False), {
            'arm': '9:29',
            'krm': '21:32',
            'rcd': '48:00',
            'rsv': '10:31',
            'srm': '-',
            'trm': '-',
            'wrk': '54:28'})

    def test_get_full_stat_dict_for_journal_page(self):
        """
        Проверка подготовки данных для страницы журнала:
        - Статистика запрашивается с учетом замены;
        - Статистика не округляется до часа;
        - От ввода/замены считаются пуски и остановы
        """
        journal = Journal.objects.get(pk=1)

        self.assertEquals(journal.full_stat(), {
            'arm': '-',
            'down_cnt': 0,
            'krm': '-',
            'rcd': '-',
            'rsv': '10:31',
            'srm': '-',
            'trm': '-',
            'up_cnt': 1,
            'wrk': '13:29'})
