# Generated by Django 2.1.4 on 2019-01-23 21:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_repository_branch'),
    ]

    operations = [
        migrations.AddField(
            model_name='commit',
            name='files_changed',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='commitsmetrics',
            name='files_changed',
            field=models.IntegerField(default=0),
        ),
    ]