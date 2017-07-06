#!/usr/bin/python
 
import sys

import cgi, cgitb 
import pyeapi
import json

##SSH
import paramiko


__author__ = 'Pradeep CH'


def executeCommand(ip,cmds,un='cvpuser',pwd='root'):  

	ip = ip.strip()
	un = un.strip()
	pwd = pwd.strip()

	connection = pyeapi.connect(host=ip,username=un,password=pwd,timeout=10) 
	resp = connection.execute(cmds)
	resp = json.dumps(resp, indent=4) 
	return resp

def validateAuthentication(ip,un='cvpuser',pwd='root'): 
	executeCommand(ip,'show hostname',un,pwd) 
	return True

def executeCommandSSH(ip,cmds,un='cvpuser',pwd='root'):

	ip = ip.strip()
	un = un.strip()
	pwd = pwd.strip()
	
	if type(cmds) is list:
		cmds = '\n'.join(cmds)

	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh.connect(ip, username=un,password=pwd)
	stdin, stdout, stderr =  ssh.exec_command(cmds) 
	data = stdout.readlines()
	ssh.close()
	return data
