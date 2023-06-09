# Generated by Django 2.1.15 on 2020-04-08 13:50

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0051_remove_room_basic'),
        ('people', '0017_notificationspreferences'),
        ('TTapp', '0013_auto_20191028_2047'),
    ]

    operations = [
        migrations.CreateModel(
            name='MinGroupsHalfDays',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('week', models.PositiveSmallIntegerField(blank=True, default=None, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(52)])),
                ('year', models.PositiveSmallIntegerField(blank=True, default=None, null=True)),
                ('weight', models.PositiveSmallIntegerField(blank=True, default=None, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(8)])),
                ('comment', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('is_active', models.BooleanField(default=True, verbose_name='Contrainte active?')),
                ('department', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='base.Department')),
                ('groups', models.ManyToManyField(blank=True, to='base.Group')),
                ('train_progs', models.ManyToManyField(blank=True, to='base.TrainingProgramme')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MinimizeBusyDays',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('week', models.PositiveSmallIntegerField(blank=True, default=None, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(52)])),
                ('year', models.PositiveSmallIntegerField(blank=True, default=None, null=True)),
                ('weight', models.PositiveSmallIntegerField(blank=True, default=None, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(8)])),
                ('comment', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('is_active', models.BooleanField(default=True, verbose_name='Contrainte active?')),
                ('department', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='base.Department')),
                ('train_progs', models.ManyToManyField(blank=True, to='base.TrainingProgramme')),
                ('tutors', models.ManyToManyField(blank=True, to='people.Tutor')),
            ],
            options={
                'verbose_name': 'Minimiser les jours de présence',
            },
        ),
        migrations.CreateModel(
            name='MinModulesHalfDays',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('week', models.PositiveSmallIntegerField(blank=True, default=None, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(52)])),
                ('year', models.PositiveSmallIntegerField(blank=True, default=None, null=True)),
                ('weight', models.PositiveSmallIntegerField(blank=True, default=None, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(8)])),
                ('comment', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('is_active', models.BooleanField(default=True, verbose_name='Contrainte active?')),
                ('department', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='base.Department')),
                ('modules', models.ManyToManyField(blank=True, to='base.Module')),
                ('train_progs', models.ManyToManyField(blank=True, to='base.TrainingProgramme')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MinNonPreferedTrainProgsSlot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('week', models.PositiveSmallIntegerField(blank=True, default=None, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(52)])),
                ('year', models.PositiveSmallIntegerField(blank=True, default=None, null=True)),
                ('weight', models.PositiveSmallIntegerField(blank=True, default=None, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(8)])),
                ('comment', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('is_active', models.BooleanField(default=True, verbose_name='Contrainte active?')),
                ('department', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='base.Department')),
                ('train_progs', models.ManyToManyField(blank=True, to='base.TrainingProgramme')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MinNonPreferedTutorsSlot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('week', models.PositiveSmallIntegerField(blank=True, default=None, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(52)])),
                ('year', models.PositiveSmallIntegerField(blank=True, default=None, null=True)),
                ('weight', models.PositiveSmallIntegerField(blank=True, default=None, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(8)])),
                ('comment', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('is_active', models.BooleanField(default=True, verbose_name='Contrainte active?')),
                ('department', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='base.Department')),
                ('train_progs', models.ManyToManyField(blank=True, to='base.TrainingProgramme')),
                ('tutors', models.ManyToManyField(related_name='min_non_prefered_tutors_slots_constraints', to='people.Tutor')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MinTutorsHalfDays',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('week', models.PositiveSmallIntegerField(blank=True, default=None, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(52)])),
                ('year', models.PositiveSmallIntegerField(blank=True, default=None, null=True)),
                ('weight', models.PositiveSmallIntegerField(blank=True, default=None, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(8)])),
                ('comment', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('is_active', models.BooleanField(default=True, verbose_name='Contrainte active?')),
                ('join2courses', models.BooleanField(default=False, verbose_name='If a tutor has 2 or 4 courses only, join it?')),
                ('department', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='base.Department')),
                ('train_progs', models.ManyToManyField(blank=True, to='base.TrainingProgramme')),
                ('tutors', models.ManyToManyField(blank=True, to='people.Tutor')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RespectBoundPerDay',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('week', models.PositiveSmallIntegerField(blank=True, default=None, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(52)])),
                ('year', models.PositiveSmallIntegerField(blank=True, default=None, null=True)),
                ('weight', models.PositiveSmallIntegerField(blank=True, default=None, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(8)])),
                ('comment', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('is_active', models.BooleanField(default=True, verbose_name='Contrainte active?')),
                ('department', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='base.Department')),
                ('train_progs', models.ManyToManyField(blank=True, to='base.TrainingProgramme')),
                ('tutors', models.ManyToManyField(blank=True, to='people.Tutor')),
            ],
            options={
                'verbose_name': 'Respecter les limites horaires',
            },
        ),
        migrations.RemoveField(
            model_name='minhalfdays',
            name='department',
        ),
        migrations.RemoveField(
            model_name='minhalfdays',
            name='groups',
        ),
        migrations.RemoveField(
            model_name='minhalfdays',
            name='modules',
        ),
        migrations.RemoveField(
            model_name='minhalfdays',
            name='train_prog',
        ),
        migrations.RemoveField(
            model_name='minhalfdays',
            name='tutors',
        ),
        migrations.RemoveField(
            model_name='minnonpreferedslot',
            name='department',
        ),
        migrations.RemoveField(
            model_name='minnonpreferedslot',
            name='train_prog',
        ),
        migrations.RemoveField(
            model_name='minnonpreferedslot',
            name='tutor',
        ),
        migrations.RemoveField(
            model_name='reasonabledays',
            name='department',
        ),
        migrations.RemoveField(
            model_name='reasonabledays',
            name='groups',
        ),
        migrations.RemoveField(
            model_name='reasonabledays',
            name='train_prog',
        ),
        migrations.RemoveField(
            model_name='reasonabledays',
            name='tutors',
        ),
        migrations.RemoveField(
            model_name='avoidbothtimes',
            name='train_prog',
        ),
        migrations.RemoveField(
            model_name='customconstraint',
            name='train_prog',
        ),
        migrations.RemoveField(
            model_name='limitcoursetypetimeperperiod',
            name='module',
        ),
        migrations.RemoveField(
            model_name='limitcoursetypetimeperperiod',
            name='train_prog',
        ),
        migrations.RemoveField(
            model_name='limitedroomchoices',
            name='train_prog',
        ),
        migrations.RemoveField(
            model_name='limitedstarttimechoices',
            name='train_prog',
        ),
        migrations.RemoveField(
            model_name='simultaneouscourses',
            name='course1',
        ),
        migrations.RemoveField(
            model_name='simultaneouscourses',
            name='course2',
        ),
        migrations.RemoveField(
            model_name='simultaneouscourses',
            name='train_prog',
        ),
        migrations.RemoveField(
            model_name='stabilize',
            name='train_prog',
        ),
        migrations.AddField(
            model_name='avoidbothtimes',
            name='train_progs',
            field=models.ManyToManyField(blank=True, to='base.TrainingProgramme'),
        ),
        migrations.AddField(
            model_name='customconstraint',
            name='train_progs',
            field=models.ManyToManyField(blank=True, to='base.TrainingProgramme'),
        ),
        migrations.AddField(
            model_name='limitcoursetypetimeperperiod',
            name='modules',
            field=models.ManyToManyField(blank=True, related_name='Course_type_limits', to='base.Module'),
        ),
        migrations.AddField(
            model_name='limitcoursetypetimeperperiod',
            name='train_progs',
            field=models.ManyToManyField(blank=True, to='base.TrainingProgramme'),
        ),
        migrations.AddField(
            model_name='limitedroomchoices',
            name='train_progs',
            field=models.ManyToManyField(blank=True, to='base.TrainingProgramme'),
        ),
        migrations.AddField(
            model_name='limitedstarttimechoices',
            name='train_progs',
            field=models.ManyToManyField(blank=True, to='base.TrainingProgramme'),
        ),
        migrations.AddField(
            model_name='simultaneouscourses',
            name='courses',
            field=models.ManyToManyField(related_name='simultaneous_courses_constraints', to='base.Course'),
        ),
        migrations.AddField(
            model_name='simultaneouscourses',
            name='train_progs',
            field=models.ManyToManyField(blank=True, to='base.TrainingProgramme'),
        ),
        migrations.AddField(
            model_name='stabilize',
            name='train_progs',
            field=models.ManyToManyField(blank=True, to='base.TrainingProgramme'),
        ),
        migrations.DeleteModel(
            name='MinHalfDays',
        ),
        migrations.DeleteModel(
            name='MinNonPreferedSlot',
        ),
        migrations.DeleteModel(
            name='ReasonableDays',
        ),
    ]
