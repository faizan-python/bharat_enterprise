# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0003_invoice_account'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='tax',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='invoice',
            name='total_item_cost',
            field=models.FloatField(default=0),
        ),
    ]
