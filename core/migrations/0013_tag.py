# Generated by Django 2.1.4 on 2019-01-14 11:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_auto_20190108_0107'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, null=True)),
                ('message', models.CharField(max_length=256, null=True)),
                ('commit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Commit')),
                ('commiter', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.Commiter')),
            ],
        ),
    ]
