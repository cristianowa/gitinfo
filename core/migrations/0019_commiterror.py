# Generated by Django 2.1.4 on 2019-02-14 00:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_commitblamepercentage'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommitError',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('commit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Commit')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.CommitErrorType')),
            ],
        ),
    ]
