# from collections import namedtuple

import psycopg2
from django.db import models
# from django.db.models.loading import cache

# from datetime import date, timedelta, datetime

from django.conf import settings


# from ..constants import PERMISSIBLE_PREC


class PCS():

    def __init__(self, db_host, db_port, db_user, db_pwd):
        self.db_host = db_host
        self.db_port = db_port
        self.db_user = db_user
        self.db_pwd = db_pwd

    def open(self):
        conn_str = 'host=%s port=%s user=%s password=%s dbname=fdata' % (
            self.db_host, self.db_port, self.db_user, self.db_pwd)
        self.conn = psycopg2.connect(conn_str)
        self.cur = self.conn.cursor()

    def close(self):
        self.conn.commit()
        self.cur.close()
        self.conn.close()

    def get_params(self):
        self.cur.execute('SELECT * FROM params;')
        return self.cur.fetchall()

pcs_source = PCS(
    db_host=settings.PCS_DATABASE['HOST'],
    db_port=settings.PCS_DATABASE['PORT'],
    db_user=settings.PCS_DATABASE['USER'],
    db_pwd=settings.PCS_DATABASE['PWD'],
    )


class Param(models.Model):
    """
    Description: Отображение параметра из таблицы params fdata
    """
    prmnum = models.IntegerField(primary_key=True)
    prmname = models.CharField(max_length=70)
    ms_accronim = models.CharField(max_length=15)
    mesunit = models.CharField(max_length=10, null=True)

    class Meta:
        verbose_name = 'параметр'
        verbose_name_plural = 'параметры'
        db_table = 'params'
        ordering = ('prmnum',)

    def load_params():
        pcs_source.open()
        dataset = pcs_source.get_params()
        prm_list = [Param(prmnum=p[0], prmname=p[2], ms_accronim=p[1], mesunit=p[8],) for p in dataset]
        Param.objects.bulk_create(prm_list)
        pcs_source.close()


"""

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
        ordering = ('prmnum', )

    def __str__(self):
        return "%s [%s:%s]" % (self.prmname, self.ms_accronim, self.prmnum)

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

        res['data'] = []  #  all the data returned by query
        res['ctrl_h'] = {}  #  the data on the edge of hour
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
"""
