# Generated by Django 3.0.5 on 2020-04-29 17:05

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('base', '0054_remove_course_group'),
        ('people', '0017_notificationspreferences'),
    ]

    operations = [
        migrations.CreateModel(
            name='ModuleTutorRepartition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('week', models.PositiveSmallIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(53)])),
                ('year', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('courses_nb', models.PositiveSmallIntegerField(default=1)),
                ('course_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.CourseType')),
                ('module', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.Module')),
                ('tutor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='people.Tutor')),
            ],
        ),
    ]
