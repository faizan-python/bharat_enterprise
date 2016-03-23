# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=250, null=True, blank=True)),
                ('email', models.EmailField(max_length=70)),
                ('website', models.URLField(null=True, blank=True)),
                ('is_active', models.BooleanField(default=False)),
                ('is_registered', models.BooleanField(default=False)),
                ('plan_start_date', models.DateTimeField(auto_now_add=True)),
                ('plan_end_date', models.DateTimeField(null=True, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Plans',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('plan_type', models.CharField(max_length=50)),
                ('price', models.FloatField()),
                ('duration', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=False)),
                ('created_by', models.ForeignKey(related_name='plans_created_by', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(related_name='plans_modified_by', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='account',
            name='plans',
            field=models.ForeignKey(blank=True, to='accounts.Plans', null=True),
        ),
        migrations.AddField(
            model_name='account',
            name='updated_by',
            field=models.ForeignKey(related_name='org_modified_by', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
