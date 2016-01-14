from django.test import TestCase

from .models import Param


class ParamTestCase(TestCase):

    def test_getting_params(self):
        params = [item.prmnum for item in Param.objects.all()]

        self.assertGreater(len(params), 0)
