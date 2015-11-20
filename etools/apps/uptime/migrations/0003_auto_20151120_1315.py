# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('uptime', '0002_employee'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='equipment',
            field=models.ForeignKey(to='uptime.Equipment', related_name='profile'),
        ),
    ]
