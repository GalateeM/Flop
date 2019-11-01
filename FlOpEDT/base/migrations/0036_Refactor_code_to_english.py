# Generated by Django 2.1.4 on 2019-06-27 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0035_auto_20190627_1131'),
    ]

    operations = [
        migrations.RenameField(
            model_name='course',
            old_name='groupe',
            new_name='group',
        ),
        migrations.RenameField(
            model_name='groupcost',
            old_name='groupe',
            new_name='group',
        ),
        migrations.RenameField(
            model_name='groupfreehalfday',
            old_name='groupe',
            new_name='group',
        ),
        migrations.RenameField(
            model_name='scheduledcourse',
            old_name='copie_travail',
            new_name='work_copy',
        ),
        migrations.RenameField(
            model_name='coursemodification',
            old_name='cours',
            new_name='course',
        ),
        migrations.RenameField(
            model_name='dependency',
            old_name='cours1',
            new_name='course1',
        ),
        migrations.RenameField(
            model_name='dependency',
            old_name='cours2',
            new_name='course2',
        ),
        migrations.RenameField(
            model_name='planningmodification',
            old_name='cours',
            new_name='course',
        ),
        migrations.RenameField(
            model_name='scheduledcourse',
            old_name='cours',
            new_name='course',
        ),
        migrations.RenameField(
            model_name='coursepreference',
            old_name='valeur',
            new_name='value',
        ),
        migrations.RenameField(
            model_name='groupcost',
            old_name='valeur',
            new_name='value',
        ),
        migrations.RenameField(
            model_name='roompreference',
            old_name='valeur',
            new_name='value',
        ),
        migrations.RenameField(
            model_name='tutorcost',
            old_name='valeur',
            new_name='value',
        ),
        migrations.RenameField(
            model_name='userpreference',
            old_name='valeur',
            new_name='value',
        ),
        migrations.RenameField(
            model_name='group',
            old_name='nom',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='module',
            old_name='nom',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='slot',
            old_name='jour',
            new_name='day',
        ),
        migrations.RenameField(
            model_name='slot',
            old_name='heure',
            new_name='hour',
        ),
    ]
