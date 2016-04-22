# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import bitfield.models


class Migration(migrations.Migration):

    dependencies = [
        ('uptime', '0004_auto_20160420_1049'),
    ]

    operations = [
        migrations.AlterField(
            model_name='intervalitem',
            name='state_code',
            field=models.CharField(max_length=3, choices=[('wrk', 'Работа'), ('hrs', 'Горячий резерв'), ('rsv', 'Резерв'), ('arm', 'Аварийный ремонт'), ('trm', 'Текущий ремонт'), ('krm', 'Капитальный ремонт'), ('srm', 'Средний ремонт'), ('rcd', 'Реконструкция'), ('ksv', 'Консервация')], default='wrk', db_index=True),
        ),
        migrations.AlterField(
            model_name='journal',
            name='control_flags',
            field=bitfield.models.BitField((('wrk', 'Работа', 'Работа'), ('hrs', 'Горячий резерв', 'ГР'), ('rsv', 'Резерв', 'РЗ'), ('arm', 'Аварийный ремонт', 'АР'), ('trm', 'Текущий ремонт', 'ТР'), ('krm', 'Капитальный ремонт', 'КР'), ('srm', 'Средний ремонт', 'СР'), ('rcd', 'Реконструкция', 'РК'), ('ksv', 'Консервация', 'КСВ')), verbose_name='контроль', default=1),
        ),
    ]
