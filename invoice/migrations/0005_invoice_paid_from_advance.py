# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0004_auto_20160324_1950'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='paid_from_advance',
            field=models.BooleanField(default=False),
        ),
    ]
