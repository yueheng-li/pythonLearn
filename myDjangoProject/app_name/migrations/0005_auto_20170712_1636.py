# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-12 08:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_name', '0004_environmentvariable_ftp_tomcat_log'),
    ]

    operations = [
        migrations.AlterField(
            model_name='environmentvariable',
            name='ftp_tomcat_log',
            field=models.CharField(max_length=100),
        ),
    ]
