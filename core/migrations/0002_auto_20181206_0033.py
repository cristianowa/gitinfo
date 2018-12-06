# Generated by Django 2.1.4 on 2018-12-06 00:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Repository',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=256)),
            ],
        ),
        migrations.AddField(
            model_name='commit',
            name='repository',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='core.Repository'),
            preserve_default=False,
        ),
    ]
