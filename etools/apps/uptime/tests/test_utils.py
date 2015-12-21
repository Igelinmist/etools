from django.test import TestCase

from ..utils import custom_redirect, req_date, req_timedelta

from datetime import date, timedelta


class CustomRedirectTestCase(TestCase):

    def test_redirect_with_get_params(self):
        self.assertEquals(
            custom_redirect('uptime:record_new', 2, rdate='18.05.2014').url,
            '/uptime/2/record_new?rdate=18.05.2014'
        )

    def test_redirect_without_get_params(self):
        self.assertEquals(
            custom_redirect('uptime:record_new', 2).url,
            '/uptime/2/record_new?'
        )


class ReqDateTestCase(TestCase):

    def test_req_date_local_str(self):
        self.assertEquals(
            req_date('15.12.2015'),
            '2015-12-15'
        )

    def test_req_date_local_date(self):

        self.assertEquals(
            req_date(date(2015, 12, 15)),
            '2015-12-15'
        )


class ReqTimedeltaTestCase(TestCase):

    def test_req_timdelta_str_correct(self):

        self.assertEquals(
            req_timedelta('24:00'),
            timedelta(hours=24)
        )

    def test_req_timdelta_str_bad(self):

        self.assertEquals(
            req_timedelta('240b'),
            timedelta(0)
        )

    def test_req_timdelta_timedelta(self):

        self.assertEquals(
            req_timedelta(timedelta(hours=24)),
            timedelta(hours=24)
        )

    def test_req_timdelta_integer(self):

        self.assertEquals(
            req_timedelta(5),
            timedelta(0)
        )

    def test_req_timdelta_float(self):

        self.assertEquals(
            req_timedelta(5.2),
            timedelta(0)
        )
