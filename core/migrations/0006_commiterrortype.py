# Generated by Django 2.1.4 on 2018-12-16 23:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_commit_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommitErrorType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
    ]