# Generated by Django 2.1.4 on 2018-12-29 01:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_auto_20181229_0130'),
    ]

    operations = [
        migrations.AddField(
            model_name='commit',
            name='merge',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
    ]
