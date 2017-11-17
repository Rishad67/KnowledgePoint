# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-17 04:33
from __future__ import unicode_literals

from django.db import migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_profile_phone_no'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='phone_no',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, help_text='+880', max_length=128),
        ),
    ]
