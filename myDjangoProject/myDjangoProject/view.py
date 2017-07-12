# -*- coding: utf-8 -*-
# Create your views here.
from django.http import HttpResponse
from django.http import HttpRequest
from app_name.models import Test,EnvironmentVariable
from django.shortcuts import render_to_response
import AntAutoBuild
import json
from SSHConn import SSHConn

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
    try:
      r = AntAutoBuild.callCmdRun("C:\\A-LICHUNHUI\\14_python\\AntAutoWar\\")
    except Exception, e:
      print e
      return HttpResponse(e)
    else:
      print 1
    finally:
      pass
    return HttpResponse(r)

def move(request):
    result = list() 
    ssh = None
    try:
      request.encoding='utf-8'
      dict = AntAutoBuild.extensionFileName()
      ev = EnvironmentVariable.objects.get(pk=1)
      ssh = SSHConn(ev.ftp_hostname, 2222, ev.ftp_username, ev.ftp_password)
      # back
      r = ssh.execCommand("mv " + ev.ftp_war_path + ev.ftp_war_name + " " + ev.ftp_war_back_path + ev.ftp_war_name + ".bak")
      result.append(r)
      result.append("\r\n")
      # move
      r1 = ssh.moveFile(dict['path'], ev.ftp_war_path + dict['nm'])
      result.append(r1)
      result.append("\r\n")
      result.append("Exec Success!")
      print result
    except Exception, e:
      print e
      return HttpResponse('Exec failure!')
    finally:
      if ssh is not None:
        ssh.close()
    return HttpResponse(result)

def getRwar(request):
    ev = EnvironmentVariable.objects.get(pk=1)
    result = list() 
    dict = {}
    dict['path'] = ev.ftp_war_path + ev.ftp_war_name
    result.append(dict)
    dict = {}
    dict['path'] = ev.ftp_war_back_path + ev.ftp_war_name + ".bak"
    result.append(dict)

    return HttpResponse(json.dumps(result), content_type='application/json')

def stop(request):
    result = list() 
    del result[:]
    ssh = None
    try:
      request.encoding='utf-8'
      dict = AntAutoBuild.extensionFileName()
      ev = EnvironmentVariable.objects.get(pk=1)
      ssh = SSHConn(ev.ftp_hostname, 2222, ev.ftp_username, ev.ftp_password)
      # stop
      stdout, stderr = ssh.execCommand(ev.ftp_tomcat_stop)
      print '=================================================================================='
      print stdout
      print stderr
      print '=================================================================================='
      result.append(stdout)
      result.append("\r\n")
      result.append(stderr)
      result.append("\r\n")
      if not stderr.strip():
        result.append("tomcat stop!")
    except Exception, e:
      print e
      return HttpResponse('Exec failure!')
    finally:
      if ssh is not None:
        ssh.close()
    return HttpResponse(result)


def start(request):
    result = list() 
    del result[:]
    ssh = None
    try:
      request.encoding='utf-8'
      dict = AntAutoBuild.extensionFileName()
      ev = EnvironmentVariable.objects.get(pk=1)
      ssh = SSHConn(ev.ftp_hostname, 2222, ev.ftp_username, ev.ftp_password)
      # start
      stdout, stderr = ssh.execCommand(ev.ftp_tomcat_start)
      print '=================================================================================='
      print stdout
      print stderr
      print '=================================================================================='
      result.append(stdout)
      result.append("\r\n")
      result.append(stderr)
      result.append("\r\n")

    except Exception, e:
      print e
      return HttpResponse('Exec failure!')
    finally:
      if ssh is not None:
        ssh.close()
    return HttpResponse(result)

def ps(request):
    result = list() 
    del result[:]
    ssh = None
    try:
      # ps
      print '=================================================================================='
      ev = EnvironmentVariable.objects.get(pk=1)
      ssh = SSHConn(ev.ftp_hostname, 2222, ev.ftp_username, ev.ftp_password)
      stdout1, stderr1 = ssh.execCommand("ps aux|grep tomcat")
      print stdout1
      print stderr1
      print '=================================================================================='
      result.append(stdout1)
      result.append("\r\n")
      result.append(stderr1)
      result.append("\r\n")

    except Exception, e:
      print e
      return HttpResponse('Exec failure!')
    finally:
      if ssh is not None:
        ssh.close()
    return HttpResponse(result)

def log(request):
    result = list() 
    del result[:]
    ssh = None
    try:
      # view log
      print '=================================================================================='
      ev = EnvironmentVariable.objects.get(pk=1)
      ssh = SSHConn(ev.ftp_hostname, 2222, ev.ftp_username, ev.ftp_password)
      stdout1, stderr1 = ssh.execCommand("tail -20 " + ev.ftp_tomcat_log)
      print stdout1
      print stderr1
      print '=================================================================================='
      result.append(stdout1)
      result.append("\r\n")
      result.append(stderr1)
      result.append("\r\n")

    except Exception, e:
      print e
      return HttpResponse('Exec failure!')
    finally:
      if ssh is not None:
        ssh.close()
    return HttpResponse(result)