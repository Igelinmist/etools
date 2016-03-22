# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pcs', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='param',
            name='mesunit',
            field=models.CharField(max_length=10, null=True),
        ),
    ]
