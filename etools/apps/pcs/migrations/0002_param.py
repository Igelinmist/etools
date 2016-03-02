# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pcs', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Param',
            fields=[
                ('prmnum', models.IntegerField(primary_key=True, serialize=False)),
                ('ms_accronim', models.CharField(max_length=15)),
                ('prmname', models.CharField(max_length=70)),
                ('last_value', models.FloatField(null=True, blank=True)),
                ('last_timestamp', models.DateTimeField(null=True, blank=True)),
                ('last_sw', models.SmallIntegerField(null=True, blank=True)),
                ('rpt_cnt', models.IntegerField(null=True, blank=True)),
                ('summer_shift', models.SmallIntegerField(null=True, blank=True)),
                ('mesunit', models.CharField(null=True, max_length=10, blank=True)),
                ('prm_abbr', models.CharField(null=True, max_length=50, blank=True)),
                ('inv', models.SmallIntegerField(null=True, blank=True)),
                ('is_accum_value', models.SmallIntegerField(null=True, blank=True)),
            ],
            options={
                'db_table': 'params',
                'managed': False,
            },
        ),
    ]
