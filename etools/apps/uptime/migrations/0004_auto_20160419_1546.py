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
            field=bitfield.models.BitField((('wrk', 'работа'), ('hrs', 'горячий резерв'), ('rsv', 'резерв'), ('arm', 'аварийный ремонт'), ('trm', 'текущий ремонт'), ('krm', 'капитальный ремонт'), ('srm', 'средний ремонт'), ('rcd', 'реконструкция')), verbose_name='контроль', default=1),
        ),
        migrations.AlterField(
            model_name='equipment',
            name='name',
            field=models.CharField(verbose_name='наименование', max_length=50),
        ),
        migrations.AlterField(
            model_name='equipment',
            name='plant',
            field=models.ForeignKey(blank=True, null=True, verbose_name='установка', to='uptime.Equipment', related_name='parts'),
        ),
        migrations.AlterField(
            model_name='journal',
            name='downtime_stat',
            field=models.BooleanField(verbose_name='Статистика простоев', default=False),
        ),
        migrations.AlterField(
            model_name='journal',
            name='equipment',
            field=models.OneToOneField(verbose_name='Оборудование', to='uptime.Equipment', related_name='journal'),
        ),
        migrations.AlterField(
            model_name='journal',
            name='hot_rzv_stat',
            field=models.BooleanField(verbose_name='Статистика горячего резерва', default=False),
        ),
        migrations.AlterField(
            model_name='journal',
            name='stat_by_parent',
            field=models.BooleanField(verbose_name='Статистика по установке', default=False),
        ),
    ]
