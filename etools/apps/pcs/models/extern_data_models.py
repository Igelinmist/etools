from collections import namedtuple
from datetime import date, timedelta, datetime

import psycopg2
import pyodbc
from django.db import models
from django.conf import settings

from pcs.constants import PERMISSIBLE_PREC


Hist = namedtuple('Hist', ['dt', 'v'])


class DBSource():

    def __init__(self, db_host, db_port, db_user, db_pwd):
        self.db_host = db_host
        self.db_port = db_port
        self.db_user = db_user
        self.db_pwd = db_pwd

    def close(self):
        self.conn.commit()
        self.cur.close()
        self.conn.close()


class PCS(DBSource):

    def open(self):
        conn_str = 'host=%s port=%s user=%s password=%s dbname=fdata' % (
            self.db_host, self.db_port, self.db_user, self.db_pwd)
        self.conn = psycopg2.connect(conn_str)
        self.cur = self.conn.cursor()

    def get_params(self):
        self.cur.execute('SELECT * FROM params;')
        return self.cur.fetchall()

    def _hist_data_set(self, hist_tbl, prmnum, dttm_from, dttm_to):
        """ Auxiliary method for getting historical data. """

        sql_str = """SELECT dttm, value
                     FROM %s
                     WHERE prmnum = %s AND dttm BETWEEN \'%s\' AND \'%s\'
                     ORDER BY dttm;""" % (hist_tbl, prmnum, dttm_from, dttm_to)
        self.cur.execute(sql_str)

        return self.cur.fetchall()

pcs_source = PCS(
    db_host=settings.PCS_DATABASE['HOST'],
    db_port=settings.PCS_DATABASE['PORT'],
    db_user=settings.PCS_DATABASE['USER'],
    db_pwd=settings.PCS_DATABASE['PWD'],
    )


class PiramidaInterface(DBSource):
    """
    Description: Класс для получения данных из комплекса Piramida2000
    """

    def open(self):
        conn_str = '''DRIVER=FreeTDS;SERVER=%s;PORT=%s;
                      DATABASE=Piramida2000;UID=%s;PWD=%s;
                      TDS_Version=8.0;ClientCharset=UTF8;''' % (
            self.db_host, self.db_port, self.db_user, self.db_pwd)
        self.conn = pyodbc.connect(conn_str)
        self.cur = self.conn.cursor()


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

    def __str__(self):
        return "%s [%s:%s]" % (self.prmname, self.ms_accronim, self.prmnum)

    def load_params():
        pcs_source.open()
        dataset = pcs_source.get_params()
        prm_list = [Param(prmnum=p[0], prmname=p[2], ms_accronim=p[1], mesunit=p[8],) for p in dataset]
        Param.objects.bulk_create(prm_list)
        pcs_source.close()

    def get_hist_data(self, dttm_from=date.today() - timedelta(1), dttm_to=date.today()):

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

        pcs_source.open()
        d_set = pcs_source._hist_data_set('hist_' + self.ms_accronim.lower(), self.prmnum, dttm_from, dttm_to)

        res = {'prm_num': self.prmnum,
               'prm_name': self.prmname, }
        # all the data returned by query
        res['data'] = []
        # the data on the edge of hour
        res['ctrl_h'] = {}
        previous_mes = {}
        for item in d_set:
            if not (PERMISSIBLE_PREC < item[0].minute < (60 - PERMISSIBLE_PREC)):
                # замеры подходят для привязки к часу
                # нужно выделить наиболее близкое значение к началу часа
                ctrl_hour = _round_hr(item[0])
                if previous_mes:
                    if previous_mes['appr'] > _get_hr_dist(item[0]):
                        # все еще приближаемся к началу часа
                        previous_mes['mes'] = (item[0], item[1])
                        previous_mes['appr'] = _get_hr_dist(item[0])
                        # заменяем значение замера в начале часа
                        res['ctrl_h'][ctrl_hour] = Hist(item[0], item[1])
                    else:
                        # начали удаляться
                        # сбрасываем previous_mes
                        previous_mes = {}
                else:
                    # предыдущего замера не было
                    previous_mes['mes'] = (item[0], item[1])
                    previous_mes['appr'] = _get_hr_dist(item[0])
                    # заменяем значение замера в начале часа
                    res['ctrl_h'][ctrl_hour] = Hist(item[0], item[1])
            res['data'].append(Hist(item[0], item[1]))
        pcs_source.close()
        return res
