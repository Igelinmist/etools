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
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128)),
                ('column_type', models.CharField(choices=[('ITV', 'Интервал'), ('DT', 'Дата'), ('PCN', 'Количество пусков'), ('OCN', 'Количество остановов')], max_length=3)),
                ('from_event', models.CharField(choices=[('FVZ', 'ввод/замена'), ('FKR', 'капремонт'), ('FSR', 'средний ремонт'), ('FRC', 'реконструкция')], max_length=3)),
                ('element_name_filter', models.CharField(blank=True, max_length=50)),
                ('weight', models.IntegerField(default=0)),
            ],
            options={
                'verbose_name_plural': 'столбцы',
                'verbose_name': 'столбец',
                'db_table': 'columns',
                'default_permissions': [],
                'ordering': ['weight'],
            },
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('department', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Equipment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('plant', models.ForeignKey(null=True, related_name='parts', to='uptime.Equipment', blank=True)),
            ],
            options={
                'verbose_name_plural': 'оборудование',
                'verbose_name': 'оборудование',
                'ordering': ['plant_id', 'name'],
                'db_table': 'equipment',
            },
        ),
        migrations.CreateModel(
            name='EventItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
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
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state_code', models.CharField(choices=[('wrk', 'Работа'), ('hrs', 'Горячий резерв'), ('rsv', 'Резерв'), ('trm', 'Тек. ремонт'), ('arm', 'Ав. ремонт'), ('krm', 'Кап. ремонт'), ('srm', 'Сред. ремонт'), ('rcd', 'Реконструкция')], db_index=True, default='wrk', max_length=3)),
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
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stat_by_parent', models.BooleanField(default=False)),
                ('hot_rzv_stat', models.BooleanField(default=False)),
                ('downtime_stat', models.BooleanField(default=False)),
                ('description', models.TextField(blank=True)),
                ('equipment', models.OneToOneField(related_name='journal', to='uptime.Equipment')),
            ],
            options={
                'db_table': 'journals',
                'permissions': (('view_journal_details', 'View journal details'), ('view_journal_list', 'View journal list'), ('create_journal_record', 'Create record'), ('edit_journal_record', 'Edit record'), ('delete_journal_record', 'Delete record'), ('create_journal_event', 'Create journal event'), ('delete_journal_event', 'Delete journal event')),
                'ordering': ['equipment__name'],
                'verbose_name_plural': 'журналы',
                'verbose_name': 'журнал',
                'default_permissions': [],
            },
        ),
        migrations.CreateModel(
            name='Record',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
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
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('is_generalizing', models.BooleanField(default=False)),
                ('weight', models.IntegerField(default=0)),
                ('equipment', models.OneToOneField(related_name='report', to='uptime.Equipment')),
            ],
            options={
                'verbose_name_plural': 'отчеты',
                'verbose_name': 'отчет',
                'default_permissions': [],
                'db_table': 'reports',
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
        migrations.AlterUniqueTogether(
            name='record',
            unique_together=set([('journal', 'rdate')]),
        ),
    ]
