# -*- coding: utf-8 -*-
# Create your views here.
from django.http import HttpResponse
from django.http import HttpRequest
from app_name.models import Test,EnvironmentVariable
from django.shortcuts import render_to_response
import AntAutoBuild
import json

# 表单
def home(request):
    return render_to_response('index.html')

def index(request):
    return render_to_response('index.html')

def getwar(request):
    dict = AntAutoBuild.extensionFileName()
    return HttpResponse(json.dumps(dict), content_type='application/json')

def run(request):
	#ev = Test.objects.get(pk=1)
    request.encoding='utf-8'
    print "1"
    try:
      r = AntAutoBuild.callCmdRun("C:\\A-LICHUNHUI\\14_python\\AntAutoWar\\")

      print "2"
    except Exception, e:
      print e
      return HttpResponse(e)
    else:
      print "3"
    finally:
      pass
    print r
    return HttpResponse(r)

