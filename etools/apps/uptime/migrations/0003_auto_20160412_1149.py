# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('uptime', '0002_auto_20151201_0900'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='journal',
            options={'verbose_name_plural': 'журналы', 'default_permissions': [], 'permissions': (('view_journal_details', 'View journal details'), ('view_journal_list', 'View journal list'), ('update_journal_description', 'Update journal description'), ('create_journal_record', 'Create record'), ('edit_journal_record', 'Edit record'), ('delete_journal_record', 'Delete record'), ('create_journal_event', 'Create journal event'), ('delete_journal_event', 'Delete journal event')), 'verbose_name': 'журнал', 'ordering': ['equipment__name']},
        ),
    ]
