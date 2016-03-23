# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Vendor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=250)),
                ('contact_person', models.CharField(max_length=50, blank=True)),
                ('email', models.EmailField(max_length=254, null=True, blank=True)),
                ('about', models.TextField(null=True, blank=True)),
                ('address', models.TextField(null=True, blank=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('phone_number', models.CharField(max_length=50)),
                ('is_active', models.BooleanField(default=True)),
                ('profile_picture', models.ImageField(null=True, upload_to=b'profile_picture/', blank=True)),
                ('account', models.ForeignKey(to='accounts.Account')),
                ('created_by', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
