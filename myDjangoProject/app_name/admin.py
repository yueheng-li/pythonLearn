# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from app_name.models import Test,EnvironmentVariable

# Register your models here.
admin.site.register(Test)
admin.site.register(EnvironmentVariable)