# -*- coding: utf-8 -*-
# Create your views here.
from django.http import HttpResponse
from django.http import HttpRequest
from app_name.models import Test,EnvironmentVariable
from django.shortcuts import render_to_response
import AntAutoBuild
import json
from SSHConn import SSHConn
import time
import dateutils

# 主页
def home(request):
    return render_to_response('index.html')

def index(request):
    return render_to_response('index.html')

# 本地war显示
def getwar(request):

    ev = getEng(request)
    dict = AntAutoBuild.extensionFileName(ev.base_directory)
    return HttpResponse(json.dumps(dict), content_type='application/json')

# 之行ant 命令调用bat文件
def run(request):
	#ev = Test.objects.get(pk=1)
    request.encoding='utf-8'
    try:
      ev = getEng(request)
      r = AntAutoBuild.callCmdRun(ev.base_directory, ev.goals)
    except Exception, e:
      print e
      return HttpResponse(e)
    else:
      print 1
    finally:
      pass
    return HttpResponse(r)

# 移动war到服务器
def move(request):
    result = list() 
    ssh = None
    try:
      request.encoding='utf-8'
      ev = getEng(request)
      dict = AntAutoBuild.extensionFileName(ev.base_directory)
      ssh = SSHConn(ev.ftp_hostname, 2222, ev.ftp_username, ev.ftp_password)

      # back
      r = ssh.execCommand("mv " + ev.ftp_war_path + ev.ftp_war_name + " " + ev.ftp_war_back_path + ev.ftp_war_name[0:-4] + "_" + dateutils.getcurrentdate() + ".war")
      result.append(r)
      result.append("\r\n")

      # move
      r1 = ssh.moveFile(dict['path'], ev.ftp_war_path + dict['nm'])
      result.append(r1)
      result.append("\r\n")

      # stop
      psout, pserror = ssh.execCommand("ps aux|grep tomcat")
      if psout.find("org.apache.catalina.startup.Bootstrap") >= 0:
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
      
      time.sleep(5) 

      # start
      psout1, pserror1 = ssh.execCommand("ps aux|grep tomcat")
      if psout.find("org.apache.catalina.startup.Bootstrap") < 0:
        stdout, stderr = ssh.execCommand(ev.ftp_tomcat_start)
        print '=================================================================================='
        print stdout
        print stderr
        print '=================================================================================='
        result.append(stdout)
        result.append("\r\n")
        result.append(stderr)
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

# 移动war到服务器
def recovery(request):
    result = list() 
    ssh = None
    try:
      request.encoding='utf-8'
      ev = getEng(request)
      dict = AntAutoBuild.extensionFileName(ev.base_directory)
      ssh = SSHConn(ev.ftp_hostname, 2222, ev.ftp_username, ev.ftp_password)

      # back
      r = ssh.execCommand("rm -fr " + ev.ftp_war_path + ev.ftp_war_name)
      r = ssh.execCommand("cp " + ev.ftp_war_back_path + ev.ftp_war_name[0:-4] + "_" + dateutils.getcurrentdate() + ".war" + " " + ev.ftp_war_path + ev.ftp_war_name)

      result.append(r)
      result.append("\r\n")

      # move
      r1 = ssh.moveFile(dict['path'], ev.ftp_war_path + dict['nm'])
      result.append(r1)
      result.append("\r\n")

      # stop
      psout, pserror = ssh.execCommand("ps aux|grep tomcat")
      if psout.find("org.apache.catalina.startup.Bootstrap") >= 0:
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
      
      time.sleep(5) 

      # start
      psout1, pserror1 = ssh.execCommand("ps aux|grep tomcat")
      if psout.find("org.apache.catalina.startup.Bootstrap") < 0:
        stdout, stderr = ssh.execCommand(ev.ftp_tomcat_start)
        print '=================================================================================='
        print stdout
        print stderr
        print '=================================================================================='
        result.append(stdout)
        result.append("\r\n")
        result.append(stderr)
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

# 获取服务器的war
def getRwar(request):
    ev = getEng(request)
    result = list() 
    dict = {}
    dict['path'] = ev.ftp_war_path + ev.ftp_war_name
    result.append(dict)
    dict = {}
    dict['path'] = ev.ftp_war_back_path + ev.ftp_war_name + ".bak"
    result.append(dict)

    return HttpResponse(json.dumps(result), content_type='application/json')

# tomcat停止
def stop(request):
    result = list() 
    del result[:]
    ssh = None
    try:
      request.encoding='utf-8'
      ev = getEng(request)
      dict = AntAutoBuild.extensionFileName(ev.base_directory)
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


# tomcat启动
def start(request):
    result = list() 
    del result[:]
    ssh = None
    try:
      request.encoding='utf-8'
      ev = getEng(request)
      dict = AntAutoBuild.extensionFileName(ev.base_directory)
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

# 查询状态
def ps(request):
    result = list() 
    del result[:]
    ssh = None
    try:
      # ps
      print '=================================================================================='
      ev = getEng(request)
      ssh = SSHConn(ev.ftp_hostname, 2222, ev.ftp_username, ev.ftp_password)
      stdout1, stderr1 = ssh.execCommand(ev.ftp_ps)
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

# log打印
def log(request):
    result = list() 
    del result[:]
    ssh = None
    try:
      # view log
      print '=================================================================================='
      ev = getEng(request)
      ssh = SSHConn(ev.ftp_hostname, 2222, ev.ftp_username, ev.ftp_password)
      stdout1, stderr1 = ssh.execCommand(ev.ftp_tomcat_log)
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

def getEng(request):
  env = request.GET.get('env', 'dev') 
  print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
  print env
  ev = EnvironmentVariable.objects.get(profile=env)
  print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"

  return ev


  
