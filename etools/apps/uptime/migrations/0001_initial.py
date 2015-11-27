# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Column',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('title', models.CharField(max_length=128)),
                ('column_type', models.CharField(max_length=3, choices=[('ITV', 'Интервал'), ('DT', 'Дата'), ('PCN', 'Количество пусков'), ('OCN', 'Количество остановов')])),
                ('from_event', models.CharField(max_length=3, choices=[('FVZ', 'ввод/замена'), ('FKR', 'капремонт'), ('FSR', 'средний ремонт'), ('FRC', 'реконструкция')])),
                ('element_name_filter', models.CharField(blank=True, max_length=50)),
                ('weight', models.IntegerField(default=0)),
            ],
            options={
                'default_permissions': [],
                'verbose_name': 'столбец',
                'verbose_name_plural': 'столбцы',
                'db_table': 'columns',
                'ordering': ['weight'],
            },
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('department', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Equipment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=50)),
                ('plant', models.ForeignKey(blank=True, null=True, to='uptime.Equipment', related_name='parts')),
            ],
            options={
                'verbose_name': 'оборудование',
                'verbose_name_plural': 'оборудование',
                'db_table': 'equipment',
                'ordering': ['plant_id', 'name'],
            },
        ),
        migrations.CreateModel(
            name='EventItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('date', models.DateField()),
                ('event_code', models.CharField(max_length=3, choices=[('vkr', 'Ввод из капремонта'), ('zmn', 'Ввод после замены'), ('vsr', 'Ввод из ср. ремонта'), ('vrc', 'Ввод из реконструкции'), ('vvd', 'Ввод'), ('sps', 'Списание')])),
            ],
            options={
                'default_permissions': [],
                'db_table': 'event_items',
            },
        ),
        migrations.CreateModel(
            name='IntervalItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('state_code', models.CharField(db_index=True, choices=[('wrk', 'Работа'), ('hrs', 'Горячий резерв'), ('rsv', 'Резерв'), ('trm', 'Тек. ремонт'), ('arm', 'Ав. ремонт'), ('krm', 'Кап. ремонт'), ('srm', 'Сред. ремонт'), ('rcd', 'Реконструкция')], max_length=3, default='wrk')),
                ('time_in_state', models.DurationField()),
            ],
            options={
                'default_permissions': [],
                'db_table': 'intervals',
            },
        ),
        migrations.CreateModel(
            name='Journal',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('stat_by_parent', models.BooleanField(default=False)),
                ('hot_rzv_stat', models.BooleanField(default=False)),
                ('downtime_stat', models.BooleanField(default=False)),
                ('description', models.TextField(blank=True)),
                ('equipment', models.OneToOneField(to='uptime.Equipment', related_name='journal')),
            ],
            options={
                'verbose_name_plural': 'журналы',
                'permissions': (('view_journal_details', 'View journal details'), ('view_journal_list', 'View journal list'), ('create_journal_record', 'Create record'), ('edit_journal_record', 'Edit record'), ('delete_journal_record', 'Delete record'), ('create_journal_event', 'Create journal event'), ('delete_journal_event', 'Delete journal event')),
                'default_permissions': [],
                'verbose_name': 'журнал',
                'db_table': 'journals',
                'ordering': ['equipment__name'],
            },
        ),
        migrations.CreateModel(
            name='Record',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
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
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('title', models.CharField(max_length=255)),
                ('is_generalizing', models.BooleanField(default=False)),
                ('weight', models.IntegerField(default=0)),
                ('equipment', models.OneToOneField(to='uptime.Equipment', related_name='report')),
            ],
            options={
                'default_permissions': [],
                'verbose_name': 'отчет',
                'db_table': 'reports',
                'verbose_name_plural': 'отчеты',
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
        migrations.AddField(
            model_name='employee',
            name='equipment',
            field=models.ForeignKey(to='uptime.Equipment', related_name='profile'),
        ),
        migrations.AddField(
            model_name='employee',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='column',
            name='report',
            field=models.ForeignKey(to='uptime.Report', related_name='columns'),
        ),
    ]
