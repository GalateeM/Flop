# Generated by Django 3.1.7 on 2021-07-09 15:19

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0081_auto_20210710_2236'),
        ('people', '0031_auto_20210709_0953'),
        ('TTapp', '0047_auto_20210510_1941'),
    ]

    operations = [
        migrations.CreateModel(
            name='LimitHolesPerDay',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weight', models.PositiveSmallIntegerField(blank=True, default=None, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(8)])),
                ('comment', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('is_active', models.BooleanField(default=True, verbose_name='Is active?')),
                ('modified_at', models.DateField(auto_now=True)),
                ('max_holes_per_day', models.PositiveSmallIntegerField(null=True)),
                ('department', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='base.department')),
                ('train_progs', models.ManyToManyField(blank=True, to='base.TrainingProgramme')),
                ('tutors', models.ManyToManyField(blank=True, to='people.Tutor')),
                ('weeks', models.ManyToManyField(to='base.Week')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
