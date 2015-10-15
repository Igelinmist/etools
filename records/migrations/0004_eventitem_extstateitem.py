# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('records', '0003_auto_20151007_1903'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventItem',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('date', models.DateField()),
                ('event_code', models.CharField(choices=[('vvd', 'Ввод'), ('vkr', 'Ввод из капремонта'), ('vsr', 'Ввод из ср. ремонта'), ('vrc', 'Ввод из реконструкции'), ('zmn', 'Ввод после замены'), ('sps', 'Списание')], max_length=3)),
                ('journal', models.ForeignKey(related_name='events', to='records.Journal')),
            ],
            options={
                'default_permissions': [],
            },
        ),
        migrations.CreateModel(
            name='ExtStateItem',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('state_code', models.CharField(choices=[('rsv', 'Резерв'), ('trm', 'Тек. ремонт'), ('arm', 'Ав. ремонт'), ('krm', 'Кап. ремонт'), ('srm', 'Сред. ремонт'), ('rcd', 'Реконструкция')], default='rsv', db_index=True, max_length=3)),
                ('time_in_state', models.DurationField()),
                ('record', models.ForeignKey(related_name='ext_states', to='records.Record')),
            ],
            options={
                'default_permissions': [],
            },
        ),
    ]
