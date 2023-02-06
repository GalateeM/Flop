# Generated by Django 3.0.14 on 2022-11-23 12:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TTapp', '0068_auto_20221123_1126'),
    ]

    operations = [
        migrations.AlterField(
            model_name='limitcoursetypetimeperperiod',
            name='fhd_period',
            field=models.CharField(choices=[('fd', 'Full day'), ('hd', 'Half day')], max_length=2, verbose_name='fhd_period'),
        ),
        migrations.AlterField(
            model_name='limitgroupstimeperperiod',
            name='fhd_period',
            field=models.CharField(choices=[('fd', 'Full day'), ('hd', 'Half day')], max_length=2, verbose_name='fhd_period'),
        ),
        migrations.AlterField(
            model_name='limitmodulestimeperperiod',
            name='fhd_period',
            field=models.CharField(choices=[('fd', 'Full day'), ('hd', 'Half day')], max_length=2, verbose_name='fhd_period'),
        ),
        migrations.AlterField(
            model_name='limittutorstimeperperiod',
            name='fhd_period',
            field=models.CharField(choices=[('fd', 'Full day'), ('hd', 'Half day')], max_length=2, verbose_name='fhd_period'),
        ),
        migrations.AlterField(
            model_name='nogroupcourseonday',
            name='fampm_period',
            field=models.CharField(choices=[('fd', 'Full day'), ('AM', 'AM'), ('PM', 'PM')], max_length=2, verbose_name='fampm_period'),
        ),
        migrations.AlterField(
            model_name='notutorcourseonday',
            name='fampm_period',
            field=models.CharField(choices=[('fd', 'Full day'), ('AM', 'AM'), ('PM', 'PM')], max_length=2, verbose_name='fampm_period'),
        ),
    ]