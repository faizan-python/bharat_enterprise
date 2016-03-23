# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('vehicle', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('payment', '0002_item'),
        ('vendor', '0001_initial'),
        ('company', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('remark', models.TextField(null=True, blank=True)),
                ('date', models.DateTimeField(null=True, blank=True)),
                ('total_paid', models.FloatField(default=0)),
                ('total_pending', models.FloatField(default=0)),
                ('invoice_number', models.AutoField(serialize=False, primary_key=True)),
                ('advance_payment', models.FloatField(default=0)),
                ('total_cost', models.FloatField(default=0)),
                ('total_weight', models.FloatField(default=0)),
                ('is_active', models.BooleanField(default=True)),
                ('is_archive', models.BooleanField(default=False)),
                ('complete_payment', models.BooleanField(default=False)),
                ('company', models.ForeignKey(to='company.Company')),
                ('created_by', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('item', models.ManyToManyField(to='payment.Item')),
                ('payment', models.ManyToManyField(to='payment.Payment')),
                ('vehicle', models.ForeignKey(blank=True, to='vehicle.Vehicle', null=True)),
                ('vendor', models.ForeignKey(to='vendor.Vendor')),
            ],
        ),
    ]
