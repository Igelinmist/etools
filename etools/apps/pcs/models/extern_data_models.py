from collections import namedtuple
from datetime import date, timedelta, datetime

import psycopg2
import pyodbc
from django.db import models
from django.conf import settings

from pcs.constants import PERMISSIBLE_PREC
from pcs.utils import AddrCoder


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

    def _get_params(self):
        """ Description: Return the list of Param objects which have not been saved in DB """
        self.open()
        self.cur.execute('SELECT * FROM params;')
        res = [Param(prmnum=p[0], prmname=p[2], ms_accronim=p[1], mesunit=p[8],) for p in self.cur.fetchall()]
        self.close()
        return res

    def _hist_data(self, hist_tbl, prmnum, dttm_from, dttm_to):
        """ Description: Return list of historical data in Hist format """
        self.open()
        res = []
        sql_str = """SELECT dttm, value
                     FROM %s
                     WHERE prmnum = %s AND dttm BETWEEN \'%s\' AND \'%s\'
                     ORDER BY dttm;""" % (hist_tbl, prmnum, dttm_from, dttm_to)
        self.cur.execute(sql_str)
        for item in self.cur.fetchall():
            res.append(Hist(item[0], item[1]))
        self.close()
        return res


class Piramida(DBSource):
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

    def _30p_data(self, enh_addr, dttm_from, dttm_to):
        res = {}
        self.open()
        syst, ctrl, chan = AddrCoder.decode_addr(enh_addr)
        sql_str = """exec sp_executesql
            N'SELECT Data_date, Value0 FROM Data
            WHERE (ParNumber=12)
                AND (DATA_DATE > @DTF) AND (DATA_DATE < @DTT)
                AND (Object=@PO) AND (Item=@PI) AND (ObjType=0)',
            N'@DTF DATETIME, @DTT DATETIME, @PO INT, @PI INT',
                '{}', '{}', {}, {};""".format(dttm_from, dttm_to, ctrl, chan)
        self.cur.execute(sql_str)
        for item in self.cur.fetchall():
            res[item[0]] = item[1]
        self.close()
        return res


class Param(models.Model):
    """
    Description: Отображение параметра из таблицы params fdata
    """
    prmnum = models.IntegerField(primary_key=True, verbose_name='Номер')
    prmname = models.CharField(max_length=70, verbose_name='Имя')
    ms_accronim = models.CharField(max_length=15, verbose_name='Код набора')
    mesunit = models.CharField(max_length=10, null=True, verbose_name='Единицы изм.')
    enh_addr = models.IntegerField(blank=True, null=True, verbose_name='Адрес замещения')

    class Meta:
        verbose_name = 'параметр'
        verbose_name_plural = 'параметры'
        db_table = 'params'
        ordering = ('prmnum',)

    def __str__(self):
        return "%s [%s:%s]" % (self.prmname, self.ms_accronim, self.prmnum)

    def get_slice_data(self, dttm_from=date.today() - timedelta(1), dttm_to=date.today()):

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
        d_list = pcs_source._hist_data('hist_' + self.ms_accronim.lower(), self.prmnum, dttm_from, dttm_to)

        res = {'prm_num': self.prmnum,
               'prm_name': self.prmname, }
        # the data on the edge of hour
        res['ctrl_tm'] = {}
        previous_mes = {}
        for item in d_list:
            if not (PERMISSIBLE_PREC < item.dt.minute < (60 - PERMISSIBLE_PREC)):
                # замеры подходят для привязки к часу
                # нужно выделить наиболее близкое значение к началу часа
                ctrl_hour = _round_hr(item.dt)
                if previous_mes:
                    if previous_mes['appr'] > _get_hr_dist(item.dt):
                        # все еще приближаемся к началу часа
                        previous_mes['mes'] = (item.dt, item.v)
                        previous_mes['appr'] = _get_hr_dist(item.dt)
                        # заменяем значение замера в начале часа
                        res['ctrl_tm'][ctrl_hour] = item
                    else:
                        # начали удаляться
                        # сбрасываем previous_mes
                        previous_mes = {}
                else:
                    # предыдущего замера не было
                    previous_mes['mes'] = (item.dt, item.v)
                    previous_mes['appr'] = _get_hr_dist(item.dt)
                    # заменяем значение замера в начале часа
                    res['ctrl_tm'][ctrl_hour] = Hist(item.dt, item.v)
        return res

    def get_30p_data(self, dttm_from=date.today() - timedelta(1), dttm_to=date.today()):

        def _round_tm_30_up(dttm):
            if dttm.minute < 30:
                return datetime(dttm.year, dttm.month, dttm.day, dttm.hour, 30)
            else:
                return datetime(dttm.year, dttm.month, dttm.day, dttm.hour) + timedelta(hours=1)

        def _delta_e(p, t1, t2):
            dt = t2 - t1
            return p * 1000 * dt.seconds/3600

        res = {'prm_num': self.prmnum,
               'prm_name': self.prmname,
               'ctrl_tm': {}, }
        # Запрос исторических данных телеметрии в базе
        d_list = pcs_source._hist_data('hist_' + self.ms_accronim.lower(), self.prmnum, dttm_from, dttm_to)
        if len(d_list) == 0:
            return res
        # >
        # Берем первый замер, переносим в буфер
        buf_t, buf_v = d_list.pop(0)
        # Находим первую метку времени получасовки и инициализируем накопитель нулем
        buf_30t = _round_tm_30_up(buf_t)
        res['ctrl_tm'][buf_30t] = 0
        for item in d_list:
            if item.dt > buf_30t:
                # Если перешагнули получасовку
                res['ctrl_tm'][buf_30t] += _delta_e(buf_v, buf_t, buf_30t)
                buf_t = buf_30t
                buf_30t = _round_tm_30_up(item.dt)
                res['ctrl_tm'][buf_30t] = 0
            else:
                # Если не перешагнули получасовку
                res['ctrl_tm'][buf_30t] += _delta_e(buf_v, buf_t, item.dt)
                buf_t, buf_v = item
        # Запрос получасовок в базе данных АИИС КУЭ
        askue_dict = askue_source._30p_data(self.enh_addr, dttm_from, dttm_to + timedelta(minutes=15))
        for key, val in res['ctrl_tm'].items():
            askue_val = askue_dict.get(key, None)
            if askue_val:
                res['ctrl_tm'][key] = '{}</br>-----</br>{}'.format(round(val), round(askue_val / 2))
            else:
                res['ctrl_tm'][key] = '{}</br>-----</br>{}'.format(round(val), '-')
        return res

pcs_source = PCS(
    db_host=settings.PCS_DATABASE['HOST'],
    db_port=settings.PCS_DATABASE['PORT'],
    db_user=settings.PCS_DATABASE['USER'],
    db_pwd=settings.PCS_DATABASE['PWD'],
    )
askue_source = Piramida(
    db_host=settings.ASKUE_DATABASE['HOST'],
    db_port=settings.ASKUE_DATABASE['PORT'],
    db_user=settings.ASKUE_DATABASE['USER'],
    db_pwd=settings.ASKUE_DATABASE['PWD'],
    )


def load_params():
    Param.objects.bulk_create(pcs_source._get_params())
