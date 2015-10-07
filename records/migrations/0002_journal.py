# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('records', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Journal',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('hot_rzv_stat', models.BooleanField(default=False)),
                ('downtime_stat', models.BooleanField(default=False)),
                ('stat_by_parent', models.BooleanField(default=False)),
                ('description', models.TextField(blank=True)),
                ('equipment', models.OneToOneField(related_name='journal', to='records.ProductionUnit')),
            ],
            options={
                'permissions': (('view_journal_details', 'Может просматривать записи журнала'), ('view_journal_list', 'Может посмотреть список журналов'), ('create_journal_record', 'Может создать запись в журнале'), ('edit_journal_record', 'Может редактировать запись в журнале'), ('delete_journal_record', 'Может удалить запись в журнале'), ('create_journal_event', 'Может создать событие в журнале'), ('delete_journal_event', 'Может удалить событие в журнале')),
                'verbose_name': 'журнал',
                'default_permissions': [],
                'verbose_name_plural': 'журналы',
                'ordering': ['equipment__name'],
            },
        ),
    ]
