# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-05-23 22:33
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('modif', '0004_all_promo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='demijourferiepromo',
            name='promo',
        ),
        migrations.RemoveField(
            model_name='dispocours',
            name='promo',
        ),
        migrations.RemoveField(
            model_name='groupe',
            name='promo',
        ),
        migrations.RemoveField(
            model_name='module',
            name='promo',
        ),
        migrations.AlterField(
            model_name='demijourferiepromo',
            name='train_prog',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modif.TrainingProgramme'),
        ),
        migrations.AlterField(
            model_name='dispocours',
            name='train_prog',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modif.TrainingProgramme'),
        ),
        migrations.AlterField(
            model_name='module',
            name='train_prog',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modif.TrainingProgramme'),
        ),
    ]
