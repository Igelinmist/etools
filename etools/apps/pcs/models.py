from django.db import models

from datetime import date


class HistoryDataManager(models.Manager):

    def get_queryset(self):
        return super(HistoryDataManager, self).get_queryset().using('fdata').order_by('dttm')


class ParamsManager(models.Manager):

    def get_queryset(self):
        return super(ParamsManager, self).get_queryset().using('fdata')


class Param(models.Model):
    prmnum = models.IntegerField(primary_key=True)
    ms_accronim = models.CharField(max_length=15)
    prmname = models.CharField(max_length=70)
    last_value = models.FloatField(blank=True, null=True)
    last_timestamp = models.DateTimeField(blank=True, null=True)
    last_sw = models.SmallIntegerField(blank=True, null=True)
    rpt_cnt = models.IntegerField(blank=True, null=True)
    summer_shift = models.SmallIntegerField(blank=True, null=True)
    mesunit = models.CharField(max_length=10, blank=True, null=True)
    prm_abbr = models.CharField(max_length=50, blank=True, null=True)
    inv = models.SmallIntegerField(blank=True, null=True)
    is_accum_value = models.SmallIntegerField(blank=True, null=True)

    objects = ParamsManager()

    class Meta:
        managed = False
        db_table = 'params'

    @property
    def model_name(self):
        return 'histmodel_' + self.ms_accronim.lower()

    @property
    def tbl_name(self):
        return 'hist_' + self.ms_accronim.lower()

    @property
    def histmodel(self):
        if hasattr(self, '_histmodel'):
            return self._histmodel
        else:
            if self.model_name in models.loading.cache.all_models['pcs']:
                self.histmodel = models.loading.cache.all_models['pcs'][self.model_name]
            else:
                # создаем модель
                class Meta:
                    managed = False
                    db_table = self.tbl_name
                attrs = {
                    'dttm': models.DateTimeField(primary_key=True),
                    'ss': models.SmallIntegerField(primary_key=True),
                    'prmnum': models.IntegerField(primary_key=True),
                    'value': models.FloatField(),
                    'sw': models.SmallIntegerField(blank=True, null=True),
                    'objects': HistoryDataManager(),
                    '__module__': 'pcs.models',
                    'Meta': Meta,
                }
                self.histmodel = type(
                    self.model_name,
                    (models.Model, ),
                    attrs
                )
        return self._histmodel

    @histmodel.setter
    def histmodel(self, value):
        self._histmodel = value

    def getHistDataSet(self, dttm_from=None, dttm_to=None):
        q_set = self.histmodel.objects
        if dttm_from:
            q_set = q_set.filter(dttm__gte=dttm_from)
        else:
            q_set = q_set.filter(dttm__gte=date.today())
        if dttm_to:
            q_set = q_set.exclude(dttm__gte=dttm_to)
        q_set = q_set.filter(prmnum=self.prmnum, ss=0)
        return q_set.all()

'''
from pcs.models import Param
p1, p2 = Param.objects.all()[0:2]
d1 = p1.getHistDataSet()
d2 = p2.getHistDataSet()
'''
