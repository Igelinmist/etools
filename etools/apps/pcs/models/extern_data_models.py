from collections import namedtuple

from django.db import models
from django.db.models.loading import cache

from datetime import date, timedelta, datetime

from ..constants import PERMISSIBLE_PREC


class HistoryDataManager(models.Manager):

    def get_queryset(self):
        return super(HistoryDataManager, self).get_queryset().using('fdata').order_by('dttm')


class ParamsManager(models.Manager):

    def get_queryset(self):
        return super(ParamsManager, self).get_queryset().using('fdata').order_by('prmnum')

Hist = namedtuple('Hist', ['dt', 'v'])


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
    params = ParamsManager()

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
            if self.model_name in cache.all_models['pcs']:
                self.histmodel = cache.all_models['pcs'][self.model_name]
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

    def _hist_data_set(self, dttm_from, dttm_to):
        q_set = self.histmodel.objects
        if dttm_from:
            q_set = q_set.filter(dttm__gte=dttm_from)
        else:
            q_set = q_set.filter(dttm__gte=date.today())
        if dttm_to:
            q_set = q_set.exclude(dttm__gte=dttm_to)
        q_set = q_set.filter(prmnum=self.prmnum, ss=0)
        return q_set.all()

    def get_hist_data(self, dttm_from=None, dttm_to=None):

        def _get_hr_dist(dttm):
            """
            function calculate time-distance to closest hour start
            """
            if dttm.minute < 30:
                res = timedelta(minutes=dttm.minute, seconds=dttm.second)
            else:
                res = timedelta(hours=1) - timedelta(minutes=dttm.minute, seconds=dttm.second)
            return res

        def _round_hr(dttm):
            if dttm.minute < 30:
                return datetime(dttm.year, dttm.month, dttm.day, dttm.hour, 0, 0)
            else:
                return datetime(dttm.year, dttm.month, dttm.day, dttm.hour, 0, 0) + timedelta(hours=1)

        d_set = self._hist_data_set(dttm_from, dttm_to)
        res = {'prm_num': self.prmnum,
               'prm_name': self.prmname, }

        res['data'] = []
        res['ctrl_h'] = {}
        previous_mes = {}
        for item in d_set:
            if not (PERMISSIBLE_PREC < item.dttm.minute < (60 - PERMISSIBLE_PREC)):
                # замеры подходят для привязки к часу
                # нужно выделить наиболее близкое значение к началу часа
                ctrl_hour = _round_hr(item.dttm)
                if previous_mes:
                    if previous_mes['appr'] > _get_hr_dist(item.dttm):
                        # все еще приближаемся к началу часа
                        previous_mes['mes'] = (item.dttm, item.value)
                        previous_mes['appr'] = _get_hr_dist(item.dttm)
                        # заменяем значение замера в начале часа
                        res['ctrl_h'][ctrl_hour] = Hist(item.dttm, item.value)
                    else:
                        # начали удаляться
                        # сбрасываем previous_mes
                        previous_mes = {}
                else:
                    # предыдущего замера не было
                    previous_mes['mes'] = (item.dttm, item.value)
                    previous_mes['appr'] = _get_hr_dist(item.dttm)
                    # заменяем значение замера в начале часа
                    res['ctrl_h'][ctrl_hour] = Hist(item.dttm, item.value)
            res['data'].append(Hist(item.dttm, item.value))

        return res
