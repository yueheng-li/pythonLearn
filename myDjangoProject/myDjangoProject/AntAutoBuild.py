#coding:utf-8 
#import os
import subprocess
import os
import time


def callCmdRun(path, goals):
  result = list() 
  bat = path + "run.bat"
  create(bat, path, goals)
  p = subprocess.Popen("cmd.exe /c" + bat, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
  curline = p.stdout.readline()
  result.append("Commond ： \r\n")
  while(curline != b''):  
  	curline = p.stdout.readline()
  	result.append(curline)
  p.wait()

  result.append("\r\n")
  result.append("ログ ： \r\n")
  with open(path + '1.log', 'r') as f:
	for line in f.readlines():  #依次读取每行  
	  #line = line.strip()       #去掉每行头尾空白  
	  result.append(line)       #保存  
  print result
  f.close()
  return result  

def create(path, base_directory, goals):
  if os.path.exists(path):
    print ""
  else:
    try:
      f = open(path, 'w')
      f.write("cd " + base_directory)
      f.write("\r\n")
      f.write(goals + " > 1.log")
    finally:
      f.close( )

def extensionFileName(base_directory):
  path = os.path.join(base_directory, "build")
  print path
  d = {}
  if os.path.exists(path):
    fn = os.listdir(path)
    for name in fn:
      if name.find('.war'):
        d['nm'] = name
        d['path'] = os.path.join(path, name)
        print d['path']
        s = os.stat(d['path'])
        ct = time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime(s.st_ctime))
        d['ct'] = ct
        return d

  
if __name__=='__main__':
  r = callCmdRun("C:\\A-LICHUNHUI\\14_python\\AntAutoWar\\")