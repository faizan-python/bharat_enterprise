# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
        ('invoice', '0002_auto_20160324_1712'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='account',
            field=models.ForeignKey(default=1, to='accounts.Account'),
            preserve_default=False,
        ),
    ]
