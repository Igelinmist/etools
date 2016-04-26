# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('uptime', '0005_auto_20160422_0819'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='journal',
            name='downtime_stat',
        ),
        migrations.RemoveField(
            model_name='journal',
            name='hot_rzv_stat',
        ),
    ]
