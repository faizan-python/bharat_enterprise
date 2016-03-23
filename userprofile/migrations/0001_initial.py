# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('user', models.OneToOneField(primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('first_name', models.CharField(max_length=50, blank=True)),
                ('last_name', models.CharField(max_length=50, blank=True)),
                ('designation', models.CharField(max_length=120, blank=True)),
                ('about', models.TextField(null=True, blank=True)),
                ('gender', models.CharField(blank=True, max_length=20, choices=[(b'Female', b'FEMALE'), (b'Male', b'MALE')])),
                ('address', models.TextField(null=True, blank=True)),
                ('phone_number', models.CharField(max_length=50, null=True, blank=True)),
                ('is_active', models.BooleanField(default=True)),
                ('profile_picture', models.ImageField(null=True, upload_to=b'profile_picture/', blank=True)),
                ('account', models.ForeignKey(to='accounts.Account')),
            ],
        ),
    ]
