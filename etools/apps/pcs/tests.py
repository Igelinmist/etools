from datetime import date, datetime
from django.test import TestCase

from .models.extern_data_models import Param


class ParamTestCase(TestCase):

    def test_getting_params(self):
        params_cnt = Param.objects.count()

        self.assertGreater(params_cnt, 0)

    def test_getting_history_data(self):
        param = Param.objects.get(pk=5324846)
        hist = param.get_hist_data()
        hist_data = hist['data']
        hist_data_cnt = len(hist_data)
        item = hist_data[0]

        self.assertGreater(hist_data_cnt, 0)
        self.assertNotEqual(item.dt, None)

    def test_getting_slice_data(self):
        param = Param.objects.get(pk=5324846)
        hist = param.get_hist_data()
        hist_data_hr = hist['ctrl_h']
        td = date.today()
        today_start = datetime(td.year, td.month, td.day)

        self.assertGreater(len(hist_data_hr), 0)
        self.assertEqual(today_start in hist_data_hr, True)
