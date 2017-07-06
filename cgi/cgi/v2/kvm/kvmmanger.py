#!/usr/bin/python2
 
import sys
import os
from os.path import expanduser 
import re
import json

sys.path.append('../Lib')
from commonutil import getRandomId

from commandexecutor import executeCommandSSH 

import cgi, cgitb 

__author__ ='Pradeep CH'
__version__='1.0.0'


sourcedirectory =  expanduser("~") + "/pat/"

showDeviceCmd = 'virsh list --all'
startDeviceCmd = 'virsh start %s'
stopDeviceCmd = 'virsh destroy %s'
serversPath  = sourcedirectory + 'kvmservers.db'

#create folder if its not exist
if not os.path.exists(sourcedirectory):
    os.makedirs(sourcedirectory)
    open(serversPath,'w')

def loadDevices(ip,un,pwd):
	data =  executeCommandSSH(ip,showDeviceCmd,un,pwd);
	fullresp ={'status':'','data':''}
	if data:
		if type(data) == list: 
			resp =[]
			for item in data[1:]:
				tempitem =re.split('\s+',item)
				if len(tempitem) < 4: 
					continue 
				resp.append({'id':tempitem[1],'device':tempitem[2],'status':tempitem[3]}) 				
			fullresp['status'] ='OK'
			fullresp['data'] = resp
		else:  
			fullresp['status'] ='ERROR'
			fullresp['data'] = resp
	else:
		fullresp['status'] ='ERROR'
		fullresp['data'] = 'No response'
	return fullresp

def start(ip,un,pwd,deviceName):
	cmd = startDeviceCmd %deviceName
	result =  executeCommandSSH(ip,cmd,un,pwd);
	resp =str(result)
	if type(result)== list:
		if len(result) >1:
			return result[0]
		return "".join(result)
	return resp

def stop(ip,un,pwd,deviceName):
	cmd = stopDeviceCmd %deviceName 
	result = executeCommandSSH(ip,cmd,un,pwd);
	if type(result)== list:
		if len(result) >1:
			return result[0]
		return "".join(result)
	return result
def stopAll(ip,un,pwd,devices):
	resp = ''
	devices = devices.split(',')
	for item in devices:
		try: 
			resp +='<br>' + str(stop(ip,un,pwd,item)) 
		except Exception as e:
			resp += '</br>Exception :' + str(e) 
	return resp
def startAll(ip,un,pwd,devices):
	resp = ''
	devices = devices.split(',')
	for item in devices:
		try: 
			resp +='<br>' + str(start(ip,un,pwd,item)) 
		except Exception as e:
			resp += '</br>Exception :' + str(e) 
	return resp

def readServers():
	try:
		if not os.path.isfile(serversPath):
			return {'status':'success','data':{}}
		with open(serversPath,'r') as f:
			data = f.read()
			if data == '':
				return {'status':'success','data':{}}
			jsonObj = json.loads(data)
			resp = [] 

			for key in jsonObj.keys():
				obj = jsonObj[key]
				obj['password']=''
				resp.append(obj)
			
			return {'status':'success','data':resp}

	except :
		return {'status':'error','data':'Something went wrong'}

#for internal purpose only
def readOrginalServer(uid):
	if not os.path.isfile(serversPath):
		return
	try:
		with open(serversPath,'r') as f:
			data = f.read()
			if data == '':
				return 
			jsonObj = json.loads(data)
			if uid  in jsonObj.keys(): 
				return jsonObj[uid]  
	except Exception as e:
		#TODO Log
		return 

def readServer(uid):
	server = readOrginalServer(uid)
	if server:
		server['password'] = ''
		return {'status':'success','data':server}
		
	else:
		return {'status':'error','data':'no data'}

def saveServer(ip,username,password,uid=None):
	try:
		if not uid:
			uid = getRandomId()

		server = {'ip':ip,'username':username,'password':password,'id':uid}

		servers = {} 
		if os.path.isfile(serversPath): 		
			with open(serversPath,'r') as f:
				content= f.read()			
				if not content == '':   
					servers =  json.loads(content) 

		with open(serversPath,'w') as f: 
			servers[uid]= server 
			f.write(json.dumps(servers))			
		return  'Server saved successfully' 
	except Exception as e:
		return  'Something went wrong. Error : %s' %(str(e))  
	
def getCurrentServer(uid):
	server  = readOrginalServer(uid)
	assert server, 'Server info not found'
	return server

def main():
	form = cgi.FieldStorage() 
	resp =''
	act = form.getvalue('action') 
	
	uid = form.getvalue('uid')
	 

	ip = form.getvalue('ip')
	un = form.getvalue('uname')
	pwd =form.getvalue('pwd')

	#TODO validate
	if act=='loadDevices':
		server = getCurrentServer(uid)
		resp =loadDevices(server['ip'],server['username'],server['password']) 
		resp = json.dumps(resp)
	elif act == 'stop':
		server = getCurrentServer(uid)
		dname = form.getvalue('device')
		resp =stop(server['ip'],server['username'],server['password'],dname)
	elif act == 'start':
		server = getCurrentServer(uid)
		dname = form.getvalue('device')
		resp =start(server['ip'],server['username'],server['password'],dname)
	elif act=='restart':
		server = getCurrentServer(uid)
		dname = form.getvalue('device')
		resp +=stop(server['ip'],server['username'],server['password'],dname)
		resp +=start(server['ip'],server['username'],server['password'],dname)
	elif act =='startall':
		server = getCurrentServer(uid)
		dnames = form.getvalue('devices')
		resp +=startAll(server['ip'],server['username'],server['password'],dnames)
	elif act =='stopall':
		server = getCurrentServer(uid)
		dnames = form.getvalue('devices')
		resp +=stopAll(server['ip'],server['username'],server['password'],dnames)
	elif act =='restartall':
		server = getCurrentServer(uid)
		dnames = form.getvalue('devices')
		resp +=stopAll(server['ip'],server['username'],server['password'],dnames)
		resp +=startAll(server['ip'],server['username'],server['password'],dnames)
	elif act=='loadServers':
		resp =readServers()
		resp = json.dumps(resp)
	elif act=='loadServer': 
		resp =readServer(uid)
		resp = json.dumps(resp)  
	elif act=='add' or act=='update':  
		resp =saveServer(ip,un,pwd,uid) 			
	else:
		resp = 'Invalid action' 
	print resp

if __name__ == "__main__":
   print 'Content-type:text/html\r\n'
   try:
      main()
   except Exception as e :
      print json.dumps({'status':'ERROR','data':'Exception %s' %str(e)})
  


