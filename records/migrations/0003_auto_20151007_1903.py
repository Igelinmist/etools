# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('records', '0002_journal'),
    ]

    operations = [
        migrations.CreateModel(
            name='Record',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('date', models.DateField()),
                ('work', models.DurationField(default='0:00')),
                ('pusk_cnt', models.IntegerField(default=0)),
                ('ostanov_cnt', models.IntegerField(default=0)),
                ('journal', models.ForeignKey(to='records.Journal', related_name='records')),
            ],
            options={
                'verbose_name_plural': 'записи',
                'verbose_name': 'запись',
                'default_permissions': [],
            },
        ),
        migrations.AlterUniqueTogether(
            name='record',
            unique_together=set([('journal', 'date')]),
        ),
    ]
