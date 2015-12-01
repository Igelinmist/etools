# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('uptime', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='equipment',
            field=models.ForeignKey(to='uptime.Equipment'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL, related_name='profile'),
        ),
    ]
