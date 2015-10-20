# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Equipment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('name', models.CharField(max_length=50)),
                ('plant', models.ForeignKey(blank=True, related_name='parts', to='uptime.Equipment', null=True)),
            ],
            options={
                'db_table': 'equipment',
                'verbose_name_plural': 'оборудование',
                'verbose_name': 'оборудование',
                'ordering': ['plant_id', 'name'],
            },
        ),
        migrations.CreateModel(
            name='EventItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('date', models.DateField()),
                ('event_code', models.CharField(choices=[('vkr', 'Ввод из капремонта'), ('zmn', 'Ввод после замены'), ('vsr', 'Ввод из ср. ремонта'), ('vrc', 'Ввод из реконструкции'), ('vvd', 'Ввод'), ('sps', 'Списание')], max_length=3)),
            ],
            options={
                'db_table': 'event_items',
                'default_permissions': [],
            },
        ),
        migrations.CreateModel(
            name='IntervalItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('state_code', models.CharField(default='wrk', choices=[('wrk', 'Работа'), ('hrs', 'Горячий резерв'), ('rsv', 'Резерв'), ('trm', 'Тек. ремонт'), ('arm', 'Ав. ремонт'), ('krm', 'Кап. ремонт'), ('srm', 'Сред. ремонт'), ('rcd', 'Реконструкция')], max_length=3, db_index=True)),
                ('time_in_state', models.DurationField()),
            ],
            options={
                'db_table': 'intervals',
                'default_permissions': [],
            },
        ),
        migrations.CreateModel(
            name='Journal',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('stat_by_parent', models.BooleanField(default=False)),
                ('hot_rzv_stat', models.BooleanField(default=False)),
                ('downtime_stat', models.BooleanField(default=False)),
                ('description', models.TextField(blank=True)),
                ('equipment', models.OneToOneField(to='uptime.Equipment', related_name='journal')),
            ],
            options={
                'verbose_name': 'журнал',
                'default_permissions': [],
                'db_table': 'journals',
                'verbose_name_plural': 'журналы',
                'permissions': (('view_journal_details', 'View journal details'), ('view_journal_list', 'View journal list'), ('create_journal_record', 'Create record'), ('edit_journal_record', 'Edit record'), ('delete_journal_record', 'Delete record'), ('create_journal_event', 'Create journal event'), ('delete_journal_event', 'Delete journal event')),
                'ordering': ['equipment__name'],
            },
        ),
        migrations.CreateModel(
            name='Record',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('rdate', models.DateField()),
                ('up_cnt', models.IntegerField(default=0)),
                ('down_cnt', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('journal', models.ForeignKey(to='uptime.Journal', related_name='records')),
            ],
            options={
                'db_table': 'records',
            },
        ),
        migrations.AddField(
            model_name='intervalitem',
            name='record',
            field=models.ForeignKey(to='uptime.Record', related_name='intervals'),
        ),
        migrations.AddField(
            model_name='eventitem',
            name='journal',
            field=models.ForeignKey(to='uptime.Journal', related_name='events'),
        ),
        migrations.AlterUniqueTogether(
            name='record',
            unique_together=set([('journal', 'rdate')]),
        ),
    ]
