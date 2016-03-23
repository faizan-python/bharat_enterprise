# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Vehicle',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('vehicle_number', models.CharField(unique=True, max_length=50)),
                ('vehicle_name', models.CharField(max_length=100, blank=True)),
                ('vehicle_colour', models.CharField(max_length=50, blank=True)),
                ('about', models.TextField(null=True, blank=True)),
                ('is_active', models.BooleanField(default=True)),
                ('last_visited_date', models.DateTimeField(null=True, blank=True)),
                ('created_by', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('vendor', models.ForeignKey(to='vendor.Vendor')),
            ],
        ),
    ]
