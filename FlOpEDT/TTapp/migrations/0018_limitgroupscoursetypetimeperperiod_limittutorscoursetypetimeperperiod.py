# Generated by Django 3.0.5 on 2020-05-10 19:56

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0017_notificationspreferences'),
        ('base', '0056_moduletutorrepartition'),
        ('TTapp', '0017_auto_20200510_1826'),
    ]

    operations = [
        migrations.CreateModel(
            name='LimitTutorsCourseTypeTimePerPeriod',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('week', models.PositiveSmallIntegerField(blank=True, default=None, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(52)])),
                ('year', models.PositiveSmallIntegerField(blank=True, default=None, null=True)),
                ('weight', models.PositiveSmallIntegerField(blank=True, default=None, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(8)])),
                ('comment', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('is_active', models.BooleanField(default=True, verbose_name='Contrainte active?')),
                ('max_hours', models.PositiveSmallIntegerField()),
                ('period', models.CharField(choices=[('fd', 'Full day'), ('hd', 'Half day')], max_length=2)),
                ('course_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.CourseType')),
                ('department', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='base.Department')),
                ('train_progs', models.ManyToManyField(blank=True, to='base.TrainingProgramme')),
                ('tutors', models.ManyToManyField(blank=True, related_name='Course_type_limits', to='people.Tutor')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='LimitGroupsCourseTypeTimePerPeriod',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('week', models.PositiveSmallIntegerField(blank=True, default=None, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(52)])),
                ('year', models.PositiveSmallIntegerField(blank=True, default=None, null=True)),
                ('weight', models.PositiveSmallIntegerField(blank=True, default=None, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(8)])),
                ('comment', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('is_active', models.BooleanField(default=True, verbose_name='Contrainte active?')),
                ('max_hours', models.PositiveSmallIntegerField()),
                ('period', models.CharField(choices=[('fd', 'Full day'), ('hd', 'Half day')], max_length=2)),
                ('course_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.CourseType')),
                ('department', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='base.Department')),
                ('groups', models.ManyToManyField(blank=True, related_name='Course_type_limits', to='base.Group')),
                ('train_progs', models.ManyToManyField(blank=True, to='base.TrainingProgramme')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]