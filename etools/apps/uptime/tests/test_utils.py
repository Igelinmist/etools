from django.test import TestCase

from ..utils import custom_redirect


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
