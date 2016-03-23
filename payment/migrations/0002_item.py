# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('payment_amount', models.FloatField(default=0)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
                ('weight', models.FloatField(default=0)),
                ('item_name', models.CharField(max_length=150, null=True, blank=True)),
            ],
        ),
    ]
