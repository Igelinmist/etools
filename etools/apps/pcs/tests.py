from datetime import date, datetime, timedelta, time
from django.test import TestCase

from pcs.models.extern_data_models import Param


class ParamTestCase(TestCase):

    def setUp(self):
        Param.load_params()

    def test_getting_params(self):
        """ test params load from external db"""
        params_cnt = Param.objects.count()

        self.assertGreater(params_cnt, 0)

    def test_getting_history_data(self):
        """ test getting historical data """
        param = Param.objects.get(pk=5324846)
        hist = param.get_hist_data()
        hist_data = hist['data']
        hist_data_cnt = len(hist_data)
        item = hist_data[0]

        self.assertGreater(hist_data_cnt, 0)
        self.assertNotEqual(item.dt, None)

    def test_getting_slice_data(self):
        """ test getting hours slices """
        param = Param.objects.get(pk=5324846)
        from_dttm = date.today() - timedelta(days=1)
        from_dttm = datetime.combine(from_dttm, time())
        to_dttm = from_dttm + timedelta(hours=12)
        hist = param.get_hist_data(from_dttm, to_dttm)
        hist_data_hr = hist['ctrl_h']

        self.assertGreater(len(hist_data_hr), 0)
        self.assertEqual(from_dttm + timedelta(hours=1) in hist_data_hr, True)
