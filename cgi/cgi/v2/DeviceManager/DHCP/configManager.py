#!/usr/bin/python2
 
import sys
import os
from os.path import expanduser 
import re
import json
import datetime

sys.path.append('../../Lib')

from commonutil import getRandomId 
from commonutil import getMD5 
from beans import DHCPServer
from sqldb import db
from ParamikkoUtil import copyRemoteFile

from dhcpconfig import DHCPDConfigParser

import cgi, cgitb 

__author__ ='Pradeep CH'
__version__='1.0.0'
 

remotepath = "/etc/dhcp/dhcpd.conf"
sourcedirectory =  expanduser("~") + "/pat/"
configdirectory = sourcedirectory +'dhcpconfig/'
targetName = 'DHCPServers'

def updateServer(s,key,keyidentifier):  
   db.updateEntry(s,targetName,key,'id') 

def getAllEnvs():  
   return db.getData('EnvInfo',['bootstrap','identifier','id']) 

def getServer(uid): 
   s = DHCPServer()
   #def getData(self,tablename,keyset,key=None,keyidentifier = ''):
   data =  db.getData(targetName,s.getAttributes().keys(),uid,'id')
   assert len(data)==1,'No info'
   data = data[0]
   return data
 
def downloadConfig(ip,un,pwd,md5):
   localPath = configdirectory + ip+'.conf'
   copyRemoteFile(ip,un,pwd,remotepath,localPath)  
   return getMD5(localPath)

def deleteAllRecords(ip):
   #db.performAction(self,target,action,condition):
   action ='delete'
   condition = 'serverIp like "%s"' %ip
   db.performAction('DHCPSubnets',action,condition)
   db.performAction('DHCPPools',action,condition)
   db.performAction('DHCPHosts',action,condition) 

def parseConfig(ip):
   localPath = configdirectory + ip+'.conf'
   assert os.path.exists(localPath),'Requested config file is not available.'
   with open(localPath,'r') as f:
      data = f.read()
   assert data,'Invalid data recived from server'
   config = DHCPDConfigParser.parse(data)
   return config

def getStatusAndEnvByBootStrap(envs,bootstrap): 
   if not bootstrap or bootstrap=='' or envs==None:
       return ['Not assigned','']
   for env in envs:
      if env['bootstrap']== bootstrap:
         return ['Assigned',env['id']]
   return ['Assigned','Env info not found']

def loadToDb(config,ip):
   envs =getAllEnvs()
   for subnet in config.subnets:
      subnetID= 'subnet_'+subnet.subnet+'_'+subnet.netmask
      row = {'id':subnetID,'serverIp':ip,'subnet':subnet.subnet,'netmask':subnet.netmask}
      db.addEntry(row,'DHCPSubnets')
      for pool in subnet.pools:
         poolId= getRandomId()
         [status,env] = getStatusAndEnvByBootStrap(envs,pool.bootfileName)
         poolrow = {'id':poolId,'subnetId':subnetID,'serverIp':ip,'assignedDate':'No info','rangeStart':pool.rangeStart,'rangeEnd':pool.rangeEnd,'bootfileName':pool.bootfileName, 'subnetMask':pool.subnetMask,'assignEndDate':'No info','routers':pool.routers,'status':status,'assignedEnv':env,'devicecount':len(pool.hosts),'hypervisor':'Not Mapped'}
         db.addEntry(poolrow,'DHCPPools')
         for host in pool.hosts:
            hostrow = {'mac':host.mac,'name':host.name,'ip':host.ip,'poolId':poolId,'serverIp':ip}
            db.addEntry(hostrow,'DHCPHosts')

def main():
	form = cgi.FieldStorage() 
	act = form.getvalue('action') 
	uid = form.getvalue('uid')
	assert uid, 'Invalid Param'
	s= getServer(uid)
	assert s,'Server info not found'

	ip = s['ip']
	un = s['username']
	pwd = s['password'] 
	
	assert ip  and un and pwd, 'Invalid information recieved'   

	if  act == 'synch':
		md5 =None
		md5 = downloadConfig(ip,un,pwd,s['configmd5'])
		if md5!= s['configmd5']:
			deleteAllRecords(ip)
			config = parseConfig(ip)
			loadToDb(config,ip)
			assert config,'Config file cannot be parced'
		s['configmd5'] = str(md5)
		s['configAvailable'] ='Avaialble'
		s['configStatus'] ='Up to date'
		s['configSynchUp'] = str(datetime.datetime.now().date())
		updateServer(s,uid,'key') 
		resp = {'status':'success','data':'Synch completed'} 
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
  


