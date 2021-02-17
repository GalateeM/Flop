# Generated by Django 3.0.5 on 2020-09-15 10:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0060_auto_20200915_1016'),
        ('people', '0018_auto_20200910_0944'),
    ]

    operations = [
        migrations.CreateModel(
            name='PreferredLinks',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('links', models.ManyToManyField(related_name='preffered_set', to='base.EnrichedLink')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='preferred_links', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
