# -*- coding: utf-8 -*-
import paramiko
import logging


class SSHConn:
	logger = logging.getLogger('scripts')

	def __init__(self, hostname, port, username, password):
		self.client = paramiko.SSHClient()
		self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		self.client.connect(hostname=hostname, port=port, username=username, password=password)
		self.transport = self.client.get_transport()
		self.channel = self.transport.open_session()


	def moveFile(self, lpath, repath):
		try:
			sftp = paramiko.SFTPClient.from_transport(self.transport)
			s = sftp.put(localpath=lpath, remotepath=repath)
		except Exception, e:
			logger.error(e)
			return 'Exec failure'
		return s

	def close(self):
		self.client.close()

	def execCommand(self, command):
		try:
			logger.info("command : " + command)
			stdin, stdout, stderr = self.client.exec_command(command)
		except Exception, e:
			logger.error(e)
			return 'Exec failure'
		return stdout.read(), stderr.read()


	def extensionFileName(remote_dir):
		d = {}
		logger.info("remote_dir : " + remote_dir)
		sftp = paramiko.SFTPClient.from_transport(self.transport)
		logger.info("remote_dir : " + remote_dir)
		fn = sftp.listdir(remote_dir) #这里需要注意，列出远程文件必须使用sftp，而不能用os
		for name in fn:
			print name
			if name.find('.war'):
				d['path'] = os.path.join(remote_dir, name)
				return d