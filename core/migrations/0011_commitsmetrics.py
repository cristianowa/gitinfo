# Generated by Django 2.1.4 on 2019-01-08 00:32

import core.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_commit_merge'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommitsMetrics',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sum', models.IntegerField(default=0)),
                ('sub', models.IntegerField(default=0)),
                ('churn', models.IntegerField(default=0)),
                ('char_sum', models.IntegerField(default=0)),
                ('char_sub', models.IntegerField(default=0)),
                ('char_churn', models.IntegerField(default=0)),
                ('merges', models.IntegerField(default=0)),
                ('period', models.CharField(choices=[(core.models.PeriodChoice('Last 30 days'), 'Last 30 days'), (core.models.PeriodChoice('Last 60 days'), 'Last 60 days'), (core.models.PeriodChoice('Last 90 days'), 'Last 90 days'), (core.models.PeriodChoice('Last 180 days'), 'Last 180 days'), (core.models.PeriodChoice('Last 360 days'), 'Last 360 days')], max_length=15)),
                ('commiter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Commiter')),
                ('repo', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.Repository')),
            ],
        ),
    ]