# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ProductionUnit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('plant', models.ForeignKey(related_name='parts', blank=True, null=True, to='records.ProductionUnit')),
            ],
            options={
                'verbose_name': 'оборудование',
                'verbose_name_plural': 'оборудование',
                'ordering': ['plant_id', 'name'],
            },
        ),
    ]
