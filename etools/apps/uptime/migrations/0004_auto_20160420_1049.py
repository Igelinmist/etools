# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import bitfield.models


class Migration(migrations.Migration):

    dependencies = [
        ('uptime', '0003_auto_20160412_1149'),
    ]

    operations = [
        migrations.AddField(
            model_name='journal',
            name='control_flags',
            field=bitfield.models.BitField((('wrk', 'Работа', 'Работа'), ('hrs', 'Горячий резерв', 'ГР'), ('rsv', 'Резерв', 'РЗ'), ('arm', 'Аварийный ремонт', 'АР'), ('trm', 'Текущий ремонт', 'ТР'), ('krm', 'Капитальный ремонт', 'КР'), ('srm', 'Средний ремонт', 'СР'), ('rcd', 'Реконструкция', 'РК')), default=1, verbose_name='контроль'),
        ),
        migrations.AlterField(
            model_name='equipment',
            name='name',
            field=models.CharField(max_length=50, verbose_name='наименование'),
        ),
        migrations.AlterField(
            model_name='equipment',
            name='plant',
            field=models.ForeignKey(to='uptime.Equipment', verbose_name='установка', null=True, related_name='parts', blank=True),
        ),
        migrations.AlterField(
            model_name='journal',
            name='downtime_stat',
            field=models.BooleanField(default=False, verbose_name='Статистика простоев'),
        ),
        migrations.AlterField(
            model_name='journal',
            name='equipment',
            field=models.OneToOneField(to='uptime.Equipment', verbose_name='Оборудование', related_name='journal'),
        ),
        migrations.AlterField(
            model_name='journal',
            name='hot_rzv_stat',
            field=models.BooleanField(default=False, verbose_name='Статистика горячего резерва'),
        ),
        migrations.AlterField(
            model_name='journal',
            name='stat_by_parent',
            field=models.BooleanField(default=False, verbose_name='Статистика по установке'),
        ),
    ]
