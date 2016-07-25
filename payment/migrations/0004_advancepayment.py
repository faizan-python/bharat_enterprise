# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('vendor', '0001_initial'),
        ('payment', '0003_auto_20160324_1950'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdvancePayment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
                ('account', models.ForeignKey(to='accounts.Account')),
                ('created_by', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('payment', models.ForeignKey(to='payment.Payment')),
                ('vendor', models.ForeignKey(to='vendor.Vendor')),
            ],
        ),
    ]
