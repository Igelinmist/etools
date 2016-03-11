# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pcs', '0002_param'),
    ]

    operations = [
        migrations.AlterField(
            model_name='band',
            name='name',
            field=models.CharField(max_length=50),
        ),
    ]
