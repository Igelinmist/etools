# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Band',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('param_num', models.IntegerField()),
                ('name', models.CharField(verbose_name='Имя для отчета', max_length=50)),
                ('weight', models.IntegerField(verbose_name='Вес', default=0)),
            ],
            options={
                'default_permissions': [],
                'verbose_name': 'лента',
                'verbose_name_plural': 'ленты',
                'ordering': ['weight'],
            },
        ),
        migrations.CreateModel(
            name='Param',
            fields=[
                ('prmnum', models.IntegerField(primary_key=True, serialize=False)),
                ('prmname', models.CharField(max_length=70)),
                ('ms_accronim', models.CharField(max_length=15)),
                ('mesunit', models.CharField(max_length=10)),
            ],
            options={
                'verbose_name': 'параметр',
                'verbose_name_plural': 'параметры',
                'db_table': 'params',
                'ordering': ('prmnum',),
            },
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('title', models.CharField(verbose_name='Заголовок', max_length=100)),
                ('weight', models.IntegerField(verbose_name='Вес', default=0)),
                ('rtype', models.CharField(verbose_name='Тип отчета', max_length=3, choices=[('hs', 'Часовые срезы'), ('ahh', 'Средняя мощность за 30 мин')])),
            ],
            options={
                'verbose_name': 'отчет',
                'verbose_name_plural': 'отчеты',
                'ordering': ['weight'],
            },
        ),
        migrations.AddField(
            model_name='band',
            name='report',
            field=models.ForeignKey(to='pcs.Report', related_name='bands'),
        ),
    ]
