from django.test import TestCase

from .models import Param


class ParamTestCase(TestCase):

    def test_getting_params(self):
        params_cnt = Param.objects.count()

        self.assertGreater(params_cnt, 0)

    def test_getting_history_data(self):
        param = Param.objects.get(pk=5324846)
        hist_data = param.getHistData()['data']
        hist_data_cnt = len(hist_data)
        item = hist_data[0]

        self.assertGreater(hist_data_cnt, 0)
        self.assertNotEqual(item.d, None)
