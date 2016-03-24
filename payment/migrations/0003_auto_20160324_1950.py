# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0002_item'),
    ]

    operations = [
        migrations.RenameField(
            model_name='item',
            old_name='payment_amount',
            new_name='price',
        ),
        migrations.AddField(
            model_name='item',
            name='total_amount',
            field=models.FloatField(default=0),
        ),
    ]
