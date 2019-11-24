# Generated by Django 2.1.3 on 2019-03-11 19:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0006_auto_20190310_1746'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grouppreferences',
            name='free_half_day_weight',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.5, max_digits=3),
        ),
        migrations.AlterField(
            model_name='grouppreferences',
            name='morning_weight',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.5, max_digits=3),
        ),
        migrations.AlterField(
            model_name='studentpreferences',
            name='free_half_day_weight',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.5, max_digits=3),
        ),
        migrations.AlterField(
            model_name='studentpreferences',
            name='morning_weight',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.5, max_digits=3),
        ),
    ]