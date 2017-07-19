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
import logging

logger = logging.getLogger('scripts')

# 主页
def home(request):
    return render_to_response('index.html')

def index(request):
    return render_to_response('index.html')

# 本地war显示
def getwar(request):
    logger.info("view.getwar is start")

    ev = getEng(request)
    dict = AntAutoBuild.extensionFileName(ev.base_directory)
    logger.info("view.getwar is end")
    return HttpResponse(json.dumps(dict), content_type='application/json')

# 之行ant 命令调用bat文件
def run(request):
	#ev = Test.objects.get(pk=1)
    request.encoding='utf-8'
    try:
      logger.info("view.run is start")
      ev = getEng(request)
      r = AntAutoBuild.callCmdRun(ev.base_directory, ev.goals)
    except Exception, e:
      logger.error(e)        #直接将错误写入到日志文件
      logger.info("view.run is end")
      return HttpResponse(e)
    else:
      logger.info("view.run is end")
    finally:
      pass
    return HttpResponse(r)

# 移动war到服务器
def move(request):
    logger.info("view.move is start")
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
        logger.info("==================================================================================")
        logger.info("stdout : " + stdout)
        logger.info("stderr : " + stderr)
        logger.info("==================================================================================")
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
        logger.info("==================================================================================")
        logger.info("stdout : " + stdout)
        logger.info("stderr : " + stderr)
        logger.info("==================================================================================")
        result.append(stdout)
        result.append("\r\n")
        result.append(stderr)
        result.append("\r\n")

      result.append("Exec Success!")
      logger.info("result : " + result)
    except Exception, e:
      logger.error(e)        #直接将错误写入到日志文件
      logger.info("view.move is end")
      return HttpResponse('Exec failure!')
    finally:
      if ssh is not None:
        ssh.close()
    logger.info("view.move is end")
    return HttpResponse(result)

# 移动war到服务器
def recovery(request):
    logger.info("view.recovery is start")
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
        logger.info("==================================================================================")
        logger.info("stdout : " + stdout)
        logger.info("stderr : " + stderr)
        logger.info("==================================================================================")
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
        logger.info("==================================================================================")
        logger.info("stdout : " + stdout)
        logger.info("stderr : " + stderr)
        logger.info("==================================================================================")
        result.append(stdout)
        result.append("\r\n")
        result.append(stderr)
        result.append("\r\n")

      result.append("Exec Success!")
      logger.info("result : " + result)
    except Exception, e:
      logger.error(e)        #直接将错误写入到日志文件
      logger.info("view.recovery is end")
      return HttpResponse('Exec failure!')
    finally:
      if ssh is not None:
        ssh.close()
    logger.info("view.recovery is end")
    return HttpResponse(result)

# 获取服务器的war
def getRwar(request):
    logger.info("view.getRwar is start")
    ev = getEng(request)
    result = list() 
    dict = {}
    dict['path'] = ev.ftp_war_path + ev.ftp_war_name
    result.append(dict)
    dict = {}
    dict['path'] = ev.ftp_war_back_path + ev.ftp_war_name + ".bak"
    result.append(dict)
    logger.info("view.getRwar is end")

    return HttpResponse(json.dumps(result), content_type='application/json')

# tomcat停止
def stop(request):
    logger.info("view.stop is start")
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
      logger.info("==================================================================================")
      logger.info("stdout : " + stdout)
      logger.info("stderr : " + stderr)
      logger.info("==================================================================================")
      result.append(stdout)
      result.append("\r\n")
      result.append(stderr)
      result.append("\r\n")
      if not stderr.strip():
        result.append("tomcat stop!")
    except Exception, e:
      logger.error(e)        #直接将错误写入到日志文件
      logger.info("view.recovery is end")
      return HttpResponse('Exec failure!')
    finally:
      if ssh is not None:
        ssh.close()
    logger.info("view.stop is end")
    return HttpResponse(result)


# tomcat启动
def start(request):
    logger.info("view.start is start")
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
      logger.info("==================================================================================")
      logger.info("stdout : " + stdout)
      logger.info("stderr : " + stderr)
      logger.info("==================================================================================")
      result.append(stdout)
      result.append("\r\n")
      result.append(stderr)
      result.append("\r\n")

    except Exception, e:
      logger.error(e)        #直接将错误写入到日志文件
      logger.info("view.recovery is end")
      return HttpResponse('Exec failure!')
    finally:
      if ssh is not None:
        ssh.close()
    logger.info("view.start is end")
    return HttpResponse(result)

# 查询状态
def ps(request):
    logger.info("view.ps is start")
    result = list() 
    del result[:]
    ssh = None
    try:
      # ps
      ev = getEng(request)
      ssh = SSHConn(ev.ftp_hostname, 2222, ev.ftp_username, ev.ftp_password)
      stdout1, stderr1 = ssh.execCommand(ev.ftp_ps)
      logger.info("==================================================================================")
      logger.info("stdout : " + stdout1)
      logger.info("stderr : " + stderr1)
      logger.info("==================================================================================")
      result.append(stdout1)
      result.append("\r\n")
      result.append(stderr1)
      result.append("\r\n")

    except Exception, e:
      logger.error(e)        #直接将错误写入到日志文件
      logger.info("view.ps is end")
      return HttpResponse('Exec failure!')
    finally:
      if ssh is not None:
        ssh.close()
    logger.info("view.ps is end")
    return HttpResponse(result)

# log打印
def log(request):
    logger.info("view.log is start")
    result = list() 
    del result[:]
    ssh = None
    try:
      # view log
      ev = getEng(request)
      ssh = SSHConn(ev.ftp_hostname, 2222, ev.ftp_username, ev.ftp_password)
      stdout1, stderr1 = ssh.execCommand(ev.ftp_tomcat_log)
      logger.info("==================================================================================")
      logger.info("stdout : " + stdout1)
      logger.info("stderr : " + stderr1)
      logger.info("==================================================================================")
      result.append(stdout1)
      result.append("\r\n")
      result.append(stderr1)
      result.append("\r\n")

    except Exception, e:
      logger.error(e)        #直接将错误写入到日志文件
      logger.info("view.log is end")
      return HttpResponse('Exec failure!')
    finally:
      if ssh is not None:
        ssh.close()
    logger.info("view.log is end")
    return HttpResponse(result)

def getEng(request):
  env = request.GET.get('env', 'dev') 
  logger.info("==================================================================================")
  ev = EnvironmentVariable.objects.get(profile=env)
  logger.info("env : " + env)
  logger.info("==================================================================================")
  return ev


  
