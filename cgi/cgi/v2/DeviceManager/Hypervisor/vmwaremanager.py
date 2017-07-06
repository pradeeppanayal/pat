#!/usr/bin/python2
 
import sys
import os
from os.path import expanduser 
import re
import json

from hypercommons import getServerInfoById

sys.path.append('../../Lib')
from commonutil import getRandomId
 
from vmactions import getAllVms,getVMInfo
from vmactions import triggerRemoteConsole 
import vmactions

from vmdkstorage import getVMBaseInfo

import cgi, cgitb 

__author__ ='Pradeep CH'
__version__='1.0.0'
 

def loadDevices(ip,un,pwd):
	fullresp  = {} 
	try:
		vms = getAllVms(ip,un,pwd)
		if(not vms or len(vms)==0):
			fullresp ={'status':'error','data':'No VM(s) found :('}
		else:
			fullresp ={'status':'success','data':vms}
			
	except Exception as e:
		fullresp ={'status':'error','data':'Something went wrong. Details :'+str(e)}
	return fullresp

def start(ip,un,pwd,moid): 
	return startAll(ip,un,pwd,moid) 

def stop(ip,un,pwd,moid): 
	return stopAll(ip,un,pwd,moid) 

def restart(ip,un,pwd,vmname): 
	return restartAll(ip,un,pwd,moid) 

def stopAll(ip,un,pwd,moids):
	resp = ''
	moids = moids.split(',')
	for moid in moids:
		try: 
			vmactions.stop(ip,un,pwd,moid)
			resp +='<br>Stop request success.' 
		except Exception as e:
			resp +='<br>Stop request failed.' 
	return {'status':'success','data':resp}

def restartAll(ip,un,pwd,moids):
	resp = ''
	moids = moids.split(',')
	for moid in moids:
		try: 
			vmactions.stop(ip,un,pwd,moid)
			resp +='<br>Stop request success.' 
			vmactions.start(ip,un,pwd,moid)
			resp +='<br>Start request success.' 
		except Exception as e:
			resp +='<br>Restart request failed.' 
	return {'status':'success','data':resp}

def startAll(ip,un,pwd,moids):
	resp = ''
	moids = moids.split(',') 
	for moid in moids:
		try:
			vmactions.start(ip,un,pwd,moid)
			resp +='<br>Start request success.' 
		except Exception as e:
			resp +='<br>Start request failed.' 
	return {'status':'success','data':resp} 

#for internal purpose only
def readOrginalServer(uid):  
	return getServerInfoById(uid) 

def readServer(uid):
	server = readOrginalServer(uid)
	if server:
		server['password'] = ''
		return {'status':'success','data':server}
		
	else:
		return {'status':'error','data':'no data'}

def getCurrentServer(uid):
	server  = readOrginalServer(uid)
	assert server, 'Server info not found'
	return server

def showConsole( clientIp, ip,un,pwd,moid):
	try:
		triggerRemoteConsole(clientIp,ip,un,pwd,moid)
		return {'status':'success','data':'Triggered successfully.'}
	except Exception as e:
		return {'status':'error','data':str(e)}

def getDeviceInfo(ip,un,pwd,dname):
	try:
		data = getVMInfo(ip,un,pwd,dname)
		return {'status':'success','data':data}	
	except Exception as e:
		return {'status':'error','data':str(e)}
def getDeviceInfoMAC(ip,un,pwd,dname):
	try:
		data = getVmInfoWithMac(ip,un,pwd,dname)
		return {'status':'success','data':data}	
	except Exception as e:
		return {'status':'error','data':str(e)}		

def main():
	form = cgi.FieldStorage() 
	resp =''
	act = form.getvalue('action') 
	
	uid = form.getvalue('uid')
	 

	ip = form.getvalue('ip')
	un = form.getvalue('uname')
	pwd =form.getvalue('pwd')
	identifier = form.getvalue('identifier')

	#TODO validate
	if act=='loadDevices':
		server = getCurrentServer(uid)
		resp =loadDevices(server['ip'],server['username'],server['password'])  
	elif act == 'stop':
		server = getCurrentServer(uid)
		moid = 	form.getvalue('moid') 
		resp =stop(server['ip'],server['username'],server['password'],moid)
	elif act == 'start':
		server = getCurrentServer(uid)
		moid = form.getvalue('moid')
		resp =start(server['ip'],server['username'],server['password'],moid)
	elif act=='restart':
		server = getCurrentServer(uid)
		moid = 	form.getvalue('moid') 
		resp =restart(server['ip'],server['username'],server['password'],moid) 
	elif act =='startall':
		server = getCurrentServer(uid)
		moids = form.getvalue('moids') 
		resp =startAll(server['ip'],server['username'],server['password'],moids)
	elif act =='stopall':
		server = getCurrentServer(uid)
		moids = form.getvalue('moids') 
		resp =stopAll(server['ip'],server['username'],server['password'],moids)
	elif act =='restartall':
		server = getCurrentServer(uid)
		moids = form.getvalue('moids') 
		resp =restartAll(server['ip'],server['username'],server['password'],moids)   
	elif act=='console':
		clientIp = cgi.escape(os.environ["REMOTE_ADDR"])
		server = getCurrentServer(uid)
		moid = 	form.getvalue('moid') 
		resp = showConsole( clientIp,server['ip'],server['username'],server['password'],moid)
	elif act=='loadDeviceInfo':
		server = getCurrentServer(uid)
		devicename = form.getvalue('deviceName') 
		resp = getDeviceInfo(server['ip'],server['username'],server['password'],devicename) 
	else:
		resp = {'status':'error','data':'Invalid action'} 
	
	resp = json.dumps(resp)		
	print resp

if __name__ == "__main__":
   print 'Content-type:text/html\r\n'
   try:
      main()
   except Exception as e :
      print json.dumps({'status':'error','data':'%s' %str(e)})
  


