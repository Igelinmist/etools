from django.db import models


class ParamsManager(models.Manager):

    def get_queryset(self):
        return super(ParamsManager, self).get_queryset().using('fdata')


class Params(models.Model):
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
