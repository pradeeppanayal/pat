#!/usr/bin/python


__author__ ='Pradeep CH'

import sys
import os
from os.path import expanduser 
import uuid
import json

sys.path.append('../../Lib')
from sshclient import SSHClient
from sqldb import db

from ParamikkoUtil import checkAuthentication,executeCommand, copyToRemote

import cgi



sourcedirectory =  expanduser("~") + "/pat/"
sourceFolder = sourcedirectory+'dhcpconfig/' 

def getServer(uid):  
   data =  db.getData('DHCPServers',['ip','username','password'],uid,'id')
   assert len(data)==1,'No server info'
   return data[0] 

#Functions
def validateAuthentication(ip,username,password):
	print "Content-type:text/html\r\n\r\n"
	try: 
		if checkAuthentication(ip,username,password):
			return {'status':'success','data': 'Authentication Success'}
		else:
			return {'status':'error','data': 'Authentication Failed'}
	except Exception as e:
		return {'status':'error','data': 'Unexpected error occured. %s' %str(e) }

def readConfigFile(ip):
   cfileName = sourceFolder+ip+'.conf'
   assert os.path.exists(cfileName),'Configuration file not found. Synch config for dhcp '+ str(ip) 
   data = '' 
   with open(cfileName,'r') as f:
      return f.read() 
   return 

def view(ip,username,password): 	
   return {'status':'success','data': readConfigFile(ip)} 

def download(ip,username,password):	
	try:
		downloadFileName = '%s_dhcpd.conf' %ip
		data  = readConfigFile(ip)
		print 'Content-Disposition: attachment; filename="%s"' % downloadFileName
		#print "Content-Length: " + str(os.stat(fullPath).st_size)
		print    # empty line between headers and body
		print data
		exit()
	except Exception as e:		
		return {'status':'error','data': 'Unexpected error occured. %s' %str(e)}

def showStatus(ip,username,password):
	return executeDHCPCommand(ip,username,password,'service dhcpd status')

def stop(ip,username,password):
	return executeDHCPCommand(ip,username,password,'service dhcpd stop')

def start(ip,username,password):
	return executeDHCPCommand(ip,username,password,'service dhcpd start')

def restart(ip,username,password):
	return executeDHCPCommand(ip,username,password,'service dhcpd restart')

def executeDHCPCommand(ip,username,password,cmd): 
	try:
		resp = executeCommand(ip,username,password,cmd);  
		return {'status':'success','data': 'Response :' + str(resp)}
	except Exception as e:
		return {'status':'error','data':  'Unexpected error occured. %s' %str(e)}

def openConsole(ip,username,password):
	clientIp = cgi.escape(os.environ["REMOTE_ADDR"])
	bodyContent =""
	bodyContent += 'Your machine IP is %s <br>' %(str(clientIp)) 
	try:
		cl = SSHClient(clientIp)
		cl.enableSSH(ip,username)
		return {'status':'success','data': 'SSH Successfull'}
	except Exception as e:
		return {'status':'error','data':'Could not connect to remote machine. Make sure the plugin is running in your machine, Cause : %s' %str(e)} 

def saveRemoteFile(ip,un,pwd,data): 
	sourceFile= str(uuid.uuid4())+'dhcpd.conf' 
	resp = {}
	try:  
		with open(sourceFile,'w') as f:
			data = f.write(data)
		copyToRemote(ip,un,pwd,sourceFile,'/etc/dhcp/dhcpd.conf')
		resp = {'status':'success','data': 'Saved'}
	except Exception as e:
		resp = {'status':'error','data': 'Could not commit the changes to remote machine. Cause : %s' %str(e)}
	try:
		os.remove(sourceFile)
	except:
		pass
	return resp 

def main():
	form = cgi.FieldStorage() 
 
	action = form.getvalue('action')
	uid= form.getvalue('uid')
	assert uid,'Invalid request'
	targetFunction = {'autheticate':validateAuthentication,	'view':view,'download' : download,'stop':stop, 		'start':start,'status':showStatus,'restart':restart,'console':openConsole}
 	resp ={}
	server = getServer(uid)

	if 'remotesave' == action:
		data = form.getvalue('config')
		assert data, 'No data to save'
		resp = saveRemoteFile(server['ip'],server['username'],server['password'],data)
	elif action in targetFunction:
		fun = targetFunction[action]
		assert server,'Invalid identifier'
		resp = fun(server['ip'],server['username'],server['password']) 		
	else: 
		resp = {'status':'error','data': 'Invalid Action'} 
   	print 'Content-type:text/html\r\n'
	print json.dumps(resp) 

if __name__ == "__main__":	
   try:
      main()
   except Exception as e :
      print 'Content-type:text/html\r\n'
      print json.dumps({'status':'error','data':'Exception %s' %str(e)})


