from django.db import models

from datetime import date


class HistoryDataManager(models.Manager):

    def get_queryset(self):
        return super(HistoryDataManager, self).get_queryset().using('fdata').order_by('dttm').only('dttm', 'value')


class Hist(models.Model):
    dttm = models.DateTimeField(primary_key=True)
    ss = models.SmallIntegerField(primary_key=True)
    prmnum = models.IntegerField(primary_key=True)
    value = models.FloatField()
    sw = models.SmallIntegerField(blank=True, null=True)

    objects = HistoryDataManager()

    class Meta:
        managed = False
        unique_together = (('dttm', 'ss', 'prmnum'),)

    def __str__(self):
        return '{0} > {1}'.format(self.dttm, self.value)


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

    def getHistDataSet(self, dttm_from=None, dttm_to=None):
        Hist._meta.db_table = 'hist_' + self.ms_accronim.lower()
        q_set = Hist.objects
        if dttm_from:
            q_set = q_set.filter(dttm__gte=dttm_from)
        else:
            q_set = q_set.filter(dttm__gte=date.today())
        if dttm_to:
            q_set = q_set.exclude(dttm__gte=dttm_to)
        q_set = q_set.filter(prmnum=self.prmnum)
        return q_set.all()
