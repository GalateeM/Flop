# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-07-06 15:15
from __future__ import unicode_literals

import caching.base
import colorfield.fields
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BreakingNews',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('week', models.PositiveSmallIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(53)])),
                ('year', models.PositiveSmallIntegerField()),
                ('x_beg', models.FloatField(blank=True, default=2.0)),
                ('x_end', models.FloatField(blank=True, default=3.0)),
                ('y', models.PositiveSmallIntegerField(blank=True, default=None, null=True)),
                ('txt', models.CharField(max_length=200)),
                ('is_linked', models.URLField(blank=True, default=None, null=True)),
                ('fill_color', colorfield.fields.ColorField(default='#228B22', max_length=18)),
                ('strk_color', colorfield.fields.ColorField(default='#000000', max_length=18)),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('no', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('semaine', models.PositiveSmallIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(53)])),
                ('an', models.PositiveSmallIntegerField()),
                ('suspens', models.BooleanField(default=False, verbose_name='En suspens?')),
            ],
            bases=(caching.base.CachingMixin, models.Model),
        ),
        migrations.CreateModel(
            name='CourseModification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('semaine_old', models.PositiveSmallIntegerField(null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(53)])),
                ('an_old', models.PositiveSmallIntegerField(null=True)),
                ('version_old', models.PositiveIntegerField()),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='CoursePreference',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('semaine', models.PositiveSmallIntegerField(null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(53)])),
                ('an', models.PositiveSmallIntegerField(null=True)),
                ('valeur', models.SmallIntegerField(default=8, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(8)])),
            ],
        ),
        migrations.CreateModel(
            name='CourseType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Day',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('no', models.PositiveSmallIntegerField(default=0)),
                ('day', models.CharField(choices=[('m', 'monday'), ('tu', 'tuesday'), ('w', 'wednesday'), ('th', 'thursday'), ('f', 'friday'), ('sa', 'saturday'), ('su', 'sunday')], default='m', max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='Dependency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('successifs', models.BooleanField(default=False, verbose_name='Successifs?')),
                ('ND', models.BooleanField(default=False, verbose_name='Jours differents')),
            ],
        ),
        migrations.CreateModel(
            name='EdtVersion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('semaine', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(53)])),
                ('an', models.PositiveSmallIntegerField()),
                ('version', models.PositiveIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=4)),
                ('size', models.PositiveSmallIntegerField()),
                ('basic', models.BooleanField(default=False, verbose_name='Basic group?')),
            ],
        ),
        migrations.CreateModel(
            name='GroupCost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('semaine', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(53)])),
                ('an', models.PositiveSmallIntegerField()),
                ('valeur', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='GroupDisplay',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('button_height', models.PositiveIntegerField(default=None, null=True)),
                ('button_txt', models.CharField(default=None, max_length=20, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='GroupFreeHalfDay',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('semaine', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(53)])),
                ('an', models.PositiveSmallIntegerField()),
                ('DJL', models.PositiveSmallIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='GroupType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Holiday',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('week', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(53)])),
                ('year', models.PositiveSmallIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Module',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100, null=True)),
                ('abbrev', models.CharField(max_length=10, verbose_name='Intitul\xe9 abbr\xe9g\xe9')),
                ('ppn', models.CharField(default='M', max_length=6)),
            ],
        ),
        migrations.CreateModel(
            name='ModuleDisplay',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('color_bg', models.CharField(default='red', max_length=20)),
                ('color_txt', models.CharField(default='black', max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Period',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('starting_week', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(53)])),
                ('ending_week', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(53)])),
            ],
        ),
        migrations.CreateModel(
            name='PlanningModification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('semaine_old', models.PositiveSmallIntegerField(null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(53)])),
                ('an_old', models.PositiveSmallIntegerField(null=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Regen',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('semaine', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(53)])),
                ('an', models.PositiveSmallIntegerField()),
                ('full', models.BooleanField(default=True, verbose_name='Compl\xe8te')),
                ('fday', models.PositiveSmallIntegerField(default=1, verbose_name='Jour')),
                ('fmonth', models.PositiveSmallIntegerField(default=1, verbose_name='Mois')),
                ('fyear', models.PositiveSmallIntegerField(default=1, verbose_name='Ann\xe9e')),
                ('stabilize', models.BooleanField(default=False, verbose_name='Stabilis\xe9e')),
                ('sday', models.PositiveSmallIntegerField(default=1, verbose_name='Jour')),
                ('smonth', models.PositiveSmallIntegerField(default=1, verbose_name='Mois')),
                ('syear', models.PositiveSmallIntegerField(default=1, verbose_name='Ann\xe9e')),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
            bases=(caching.base.CachingMixin, models.Model),
        ),
        migrations.CreateModel(
            name='RoomGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
            bases=(caching.base.CachingMixin, models.Model),
        ),
        migrations.CreateModel(
            name='RoomPreference',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('semaine', models.PositiveSmallIntegerField(null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(53)])),
                ('an', models.PositiveSmallIntegerField(null=True)),
                ('valeur', models.SmallIntegerField(default=8, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(8)])),
            ],
        ),
        migrations.CreateModel(
            name='RoomSort',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='RoomType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
            bases=(caching.base.CachingMixin, models.Model),
        ),
        migrations.CreateModel(
            name='ScheduledCourse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('no', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('noprec', models.BooleanField(default=True, verbose_name='vrai si on ne veut pas garder la salle')),
                ('copie_travail', models.PositiveSmallIntegerField(default=0)),
            ],
            bases=(caching.base.CachingMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Slot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('duration', models.PositiveSmallIntegerField(default=90, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(240)])),
            ],
            bases=(caching.base.CachingMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Time',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('apm', models.CharField(choices=[('AM', 'AM'), ('PM', 'PM')], default='AM', max_length=2, verbose_name='Half day')),
                ('no', models.PositiveSmallIntegerField(default=0)),
                ('hours', models.PositiveSmallIntegerField(default=8, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(23)])),
                ('minutes', models.PositiveSmallIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(59)])),
            ],
        ),
        migrations.CreateModel(
            name='TrainingHalfDay',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('apm', models.CharField(blank=True, choices=[('AM', 'AM'), ('PM', 'PM')], default=None, max_length=2, null=True, verbose_name='Demi-journ\xe9e')),
                ('week', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(53)])),
                ('year', models.PositiveSmallIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='TrainingProgramme',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('abbrev', models.CharField(max_length=5)),
            ],
        ),
        migrations.CreateModel(
            name='TrainingProgrammeDisplay',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('row', models.PositiveSmallIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='TutorCost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('semaine', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(53)])),
                ('an', models.PositiveSmallIntegerField()),
                ('valeur', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='UserPreference',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('semaine', models.PositiveSmallIntegerField(null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(53)])),
                ('an', models.PositiveSmallIntegerField(null=True)),
                ('valeur', models.SmallIntegerField(default=8, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(8)])),
                ('creneau', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modif.Slot')),
            ],
        ),
    ]
