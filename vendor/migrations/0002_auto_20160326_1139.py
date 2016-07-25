# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='vendor',
            name='advance_amount',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='vendor',
            name='pending_amount',
            field=models.FloatField(default=0),
        ),
    ]
