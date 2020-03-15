# Generated by Django 2.1.15 on 2020-03-14 23:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0016_auto_20200302_1718'),
        ('base', '0051_remove_room_basic'),
        ('TTapp', '0014_auto_20200314_2222'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='avoidbothtimes',
            name='department',
        ),
        migrations.RemoveField(
            model_name='avoidbothtimes',
            name='group',
        ),
        migrations.RemoveField(
            model_name='avoidbothtimes',
            name='train_prog',
        ),
        migrations.RemoveField(
            model_name='avoidbothtimes',
            name='tutor',
        ),
        migrations.RemoveField(
            model_name='limitedroomchoices',
            name='department',
        ),
        migrations.RemoveField(
            model_name='limitedroomchoices',
            name='group',
        ),
        migrations.RemoveField(
            model_name='limitedroomchoices',
            name='module',
        ),
        migrations.RemoveField(
            model_name='limitedroomchoices',
            name='possible_rooms',
        ),
        migrations.RemoveField(
            model_name='limitedroomchoices',
            name='train_prog',
        ),
        migrations.RemoveField(
            model_name='limitedroomchoices',
            name='tutor',
        ),
        migrations.RemoveField(
            model_name='limitedroomchoices',
            name='type',
        ),
        migrations.RemoveField(
            model_name='limitedstarttimechoices',
            name='department',
        ),
        migrations.RemoveField(
            model_name='limitedstarttimechoices',
            name='group',
        ),
        migrations.RemoveField(
            model_name='limitedstarttimechoices',
            name='module',
        ),
        migrations.RemoveField(
            model_name='limitedstarttimechoices',
            name='train_prog',
        ),
        migrations.RemoveField(
            model_name='limitedstarttimechoices',
            name='tutor',
        ),
        migrations.RemoveField(
            model_name='limitedstarttimechoices',
            name='type',
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
            model_name='simultaneouscourses',
            name='course1',
        ),
        migrations.RemoveField(
            model_name='simultaneouscourses',
            name='course2',
        ),
        migrations.RemoveField(
            model_name='simultaneouscourses',
            name='department',
        ),
        migrations.RemoveField(
            model_name='simultaneouscourses',
            name='train_prog',
        ),
        migrations.RemoveField(
            model_name='customconstraint',
            name='train_prog',
        ),
        migrations.RemoveField(
            model_name='limitcoursetypetimeperperiod',
            name='train_prog',
        ),
        migrations.RemoveField(
            model_name='minhalfdays',
            name='train_prog',
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
            model_name='stabilize',
            name='train_prog',
        ),
        migrations.AddField(
            model_name='customconstraint',
            name='train_progs',
            field=models.ManyToManyField(blank=True, to='base.TrainingProgramme'),
        ),
        migrations.AddField(
            model_name='limitcoursetypetimeperperiod',
            name='train_progs',
            field=models.ManyToManyField(blank=True, to='base.TrainingProgramme'),
        ),
        migrations.AddField(
            model_name='minhalfdays',
            name='train_progs',
            field=models.ManyToManyField(blank=True, to='base.TrainingProgramme'),
        ),
        migrations.AddField(
            model_name='minnonpreferedslot',
            name='train_progs',
            field=models.ManyToManyField(blank=True, to='base.TrainingProgramme'),
        ),
        migrations.AddField(
            model_name='minnonpreferedslot',
            name='tutors',
            field=models.ManyToManyField(related_name='min_non_prefered_slots_constraints', to='people.Tutor'),
        ),
        migrations.AddField(
            model_name='stabilize',
            name='train_progs',
            field=models.ManyToManyField(blank=True, to='base.TrainingProgramme'),
        ),
        migrations.DeleteModel(
            name='AvoidBothTimes',
        ),
        migrations.DeleteModel(
            name='LimitedRoomChoices',
        ),
        migrations.DeleteModel(
            name='LimitedStartTimeChoices',
        ),
        migrations.DeleteModel(
            name='ReasonableDays',
        ),
        migrations.DeleteModel(
            name='SimultaneousCourses',
        ),
    ]
