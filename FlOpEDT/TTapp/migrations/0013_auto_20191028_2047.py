# Generated by Django 2.1.4 on 2019-10-28 20:47

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TTapp', '0012_auto_20190603_2046'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stabilize',
            name='fixed_days',
        ),
        migrations.AddField(
            model_name='stabilize',
            name='fixed_days',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(choices=[('m', 'monday'), ('tu', 'tuesday'), ('w', 'wednesday'), ('th', 'thursday'), ('f', 'friday'), ('sa', 'saturday'), ('su', 'sunday')], max_length=2), blank=True, null=True, size=None),
        ),
    ]
