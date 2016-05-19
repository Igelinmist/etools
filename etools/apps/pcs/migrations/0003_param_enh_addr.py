# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pcs', '0002_auto_20160322_1350'),
    ]

    operations = [
        migrations.AddField(
            model_name='param',
            name='enh_addr',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
