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
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('param_num', models.IntegerField()),
                ('name', models.CharField(max_length=15)),
                ('weight', models.IntegerField(default=0)),
            ],
            options={
                'ordering': ['weight'],
                'verbose_name': 'лента',
                'verbose_name_plural': 'ленты',
                'default_permissions': [],
            },
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('weight', models.IntegerField(default=0)),
                ('rtype', models.CharField(choices=[('hs', 'Часовые срезы'), ('ahh', 'Средняя мощность за 30 мин')], max_length=3)),
            ],
            options={
                'ordering': ['weight'],
                'verbose_name_plural': 'отчеты',
                'verbose_name': 'отчет',
            },
        ),
        migrations.AddField(
            model_name='band',
            name='report',
            field=models.ForeignKey(to='pcs.Report', related_name='bands'),
        ),
    ]
