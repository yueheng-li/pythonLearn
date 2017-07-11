# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Test(models.Model):
    uuid = models.CharField(max_length=20)
    name = models.CharField(max_length=20)

# Create your models here.
class EnvironmentVariable(models.Model):
    base_directory = models.CharField(max_length=50)
    goals = models.CharField(max_length=20)
    ftp_hostname = models.CharField(max_length=20)
    ftp_port = models.CharField(max_length=20)
    ftp_username = models.CharField(max_length=20)
    ftp_password = models.CharField(max_length=20)
    ftp_tomcat_stop = models.CharField(max_length=50)
    ftp_tomcat_start = models.CharField(max_length=50)
    ftp_ps = models.CharField(max_length=50)
    ftp_war_path = models.CharField(max_length=50)
    ftp_war_back_path = models.CharField(max_length=50)
