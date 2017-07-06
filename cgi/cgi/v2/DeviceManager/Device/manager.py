#!/usr/bin/python2
 
import sys
import os
from os.path import expanduser 
import re
import json
from threading import Thread
import uuid
import cgi, cgitb 
import datetime
sys.path.append('../../Lib')
 
from sqldb import db
from beans import EnvInfo
from usermanager import authenticate

from dhcpconfig import Config,Pool,Host,Subnet
from ParamikkoUtil import checkAuthentication,readRemoteFile,executeCommand, copyToRemote
from vmactions import getVMInfo,start,stop

sourcedirectory =  expanduser("~") + "/pat/"
configdirectory = sourcedirectory +'dhcpconfig/'
allocationLogLocation = sourcedirectory +'/pat/logs/allocationlog/'

copyCommand = 'yes | cp -rf %s %s' 
vmdkFlatFileFormat ='%s-flat.vmdk'
vmdkFileFormat ='%s.vmdk'
removeComand = 'rm -rf %s'
vmdkConvertCommandFormat = 'vmkfstools -i %s -d eagerzeroedthick %s'

__author__ ='Pradeep CH'
__version__='1.0.0'

def log(msg):
   with open('log','a') as f:
      f.write('\n'+ str(datetime.datetime.now())+':'+ msg)

def logToFile(fileName,msg):
   #log(msg)
   with open(fileName,'a') as f:
      f.write('\n'+ str(datetime.datetime.now())+':'+ msg)


def getAllServers(): 
       s = EnvInfo()
       #def getData(self,tablename,keyset,key=None,keyidentifier = ''):
       return db.getData('EnvInfo',['id','identifier','phase','team','ip','bootstrap']) 

def getEnv(envs,envId):
   for env in envs:
      if env['id'] == envId:
         return env

def executeDHCPCommand(ip,username,password,cmd): 
   try:
      resp = executeCommand(ip,username,password,cmd);  
      return {'status':'success','data': 'Response :' + str(resp)}
   except Exception as e:
      return {'status':'error','data':  'Unexpected error occured. %s' %str(e)}

def getEnvInfo(envs,envId):
   if envs==None:
      return ['-','-','-','-']
   env =getEnv(envs,envId)
   if env:
         return [env['identifier'],env['phase'],env['team'],env['ip']]
   return ['Not found','-','-','Not found']

   
def getPools():
   try:
      envs= getAllServers()
      data= db.getNamedTrigger('POOLINFO')
      for pool in data:
         envId = pool['assignedEnv']
         [envIdentifier,phase,team,ip] = getEnvInfo(envs,envId)
         pool['envIdentifier'] = envIdentifier
         pool['envteam'] = team
         pool['envphase'] = phase
         pool['envip'] = ip
      return {'status':'success','data':data}
   except Exception as e:
      return {'status':'error','data':str(e)}

def getPool(uid):
   data = db.getData('DHCPPools',['id','serverIp','rangeEnd','rangeStart','status','devicecount','hypervisor'],uid,'id') 
   assert data and len(data)==1,'invalid data recived from database'
   return data[0]

def getPoolInfo(uid):
   try:
      data = getPool(uid)
      return {'status':'success','data':data}
   except Exception as e:
      return {'status':'error','data':str(e)}

def mapHyperisor(uid,hypervisor):
   try:
      mapper = {'hypervisor':hypervisor}
      db.updateEntry(mapper,'DHCPPools',uid,'id');
      return {'status':'success','data':'Changes saved.'}
   except Exception as e:
      return {'status':'error','data':str(e)}

def assign(envId,uid,santizeReq,numberofdays,dhcpIp,dhcpun,dhcppwd,logFile):
   #Convert to full path
   logFile = allocationLogLocation + logFile
   try: 
      logToFile(logFile,'Assign initated..')
      logToFile(logFile,'Reading env info..')
      envs= getAllServers()
      env = getEnv(envs,envId)
      logToFile(logFile,'Reading env info completed')
      logToFile(logFile,'Reading Pool info..')
      pool = getPool(uid) 
      assert pool, 'Pool info not found'
      assert env, 'Envirnment details not found'

      logToFile(logFile,'Reading Pool Completed')
      logToFile(logFile,'Updating database..')

      assignedDate = str(datetime.datetime.now().date())
      assignEndDate = str((datetime.datetime.now()+ datetime.timedelta(days=int(numberofdays))).date())
      mapper ={'bootfileName':env['bootstrap'],'status':'Assigned','assignedDate':assignedDate,'assignEndDate':assignEndDate,'assignedEnv':envId}
      db.updateEntry(mapper,'DHCPPools',uid,'id');
      logToFile(logFile,'Updating database completed')

      logToFile(logFile,'Making changes to DHCP server')
      generateAndPushConfig(dhcpIp,dhcpun,dhcppwd)
      logToFile(logFile,'Making changes to DHCP server completed')
      
      
      sanmsg = 'No sanitazation'
      if santizeReq:
         logToFile(logFile,'Sanitizing initiated')
         hostCondition = 'serverIp like "%s" and poolId like "%s"' %(pool['serverIp'],pool['id'])
         hosts = db.getDataWithCondition('DHCPHosts',['mac','ip','name'],hostCondition) 
         assert hosts,'There is no device found for host'
         sanmsg = santize(hosts,pool['hypervisor'],logFile)
         logToFile(logFile,'Sanitizing completed')


      return {'status':'success','data':'Assign completed. Sanitization info :'+sanmsg}
   except Exception as e:
      return {'status':'error','data':str(e)}

def generateAndPushConfig(ip,dhcpun,dhcppwd):
   condition ='serverIp like "%s"' %ip         
   config = Config()
   #def getDataWithCondition(self,tablename,keyset,condition):
   #load data
   subnets = db.getDataWithCondition('DHCPSubnets',['subnet','netmask','id'],condition)
   cSubnets =[]
   for subnet in subnets:
      poolCondition = 'serverIp like "%s" and subnetId like "%s"' %(ip,subnet['id'])
      pools = db.getDataWithCondition('DHCPPools',["id","assignedDate",'rangeStart','rangeEnd','bootfileName','subnetMask','routers','status'],poolCondition)
      cPools = []
      for pool in pools:
         hostCondition = 'serverIp like "%s" and poolId like "%s"' %(ip,pool['id'])
         hosts = db.getDataWithCondition('DHCPHosts',['mac','ip','name'],hostCondition)
         cHosts = []
         for host in hosts:
            host['bootfileName'] =''
            cHost = Host()
            cHost.loadData(host)
            cHosts.append(cHost)
         cPool = Pool()
         pool['hosts'] = cHosts
         cPool.loadData(pool)
         cPools.append(cPool)
      cSubnet = Subnet()
      subnet['pools'] = cPools
      subnet['hosts'] = []
      cSubnet.loadData(subnet)
      cSubnets.append(cSubnet)
   config.subnets = cSubnets
   localPath = configdirectory + ip+'.conf'
   with open(localPath,'w') as f:
      f.write(config.getAsConfig())
   assert os.path.exists(localPath),'Configlet file write failed'

   copyToRemote(ip,dhcpun,dhcppwd,localPath,'/etc/dhcp/dhcpd.conf')
   executeDHCPCommand(ip,dhcpun,dhcppwd,'service dhcpd restart') 

   pass

def release(uid,santizeReq,dhcpip,dhcpun,dhcppwd,logFile):
   #Convert to full path
   logFile = allocationLogLocation + logFile
   logToFile(logFile,'Release initiated...')

   try: 
      mapper ={'bootfileName':'','status':'Not Assigned','assignedDate':'-','assignEndDate':'-','assignedEnv':'-'}
      logToFile(logFile,'Updating database..')
      db.updateEntry(mapper,'DHCPPools',uid,'id');
      logToFile(logFile,'Updating database completed')
      logToFile(logFile,'Updating DHCP config...')
      generateAndPushConfig(dhcpip,dhcpun,dhcppwd)
      logToFile(logFile,'Updating DHCP completed')

      if santizeReq:
         logToFile(logFile,'Sanitizing initiated')
         hostCondition = 'serverIp like "%s" and poolId like "%s"' %(pool['serverIp'],pool['id'])
         hosts = db.getDataWithCondition('DHCPHosts',['mac','ip','name'],hostCondition) 
         assert hosts,'There is no device found for host'
         sanmsg = santize(hosts,pool['hypervisor'],logFile)
         logToFile(logFile,'Sanitizing completed')
      logToFile(logFile,'Release completed')
      return {'status':'success','data':'Release completed.'}
   except Exception as e:
      logToFile(logFile,'Release failed %s' %str(e))
      return {'status':'error','data':str(e)}

def getHyperVisiorByIp(ip):
   condition ='ip like "%s"' %ip
   data =  db.getDataWithCondition('Hypervisors',['id','ip','username','password','type'],condition)
   assert len(data)==1,'No hypervisor info found'
   return data[0]

def resetVm(vmname,hyperVisor):
   resp ='\nSanitizing ' + str(vmname)
   ip = hyperVisor['ip']
   un = hyperVisor['username']
   pwd = hyperVisor['password']
   vm = getVMInfo(ip,un,pwd,vmname)
   resp +='Stoping VM'
   try:
       stop(ip,un,pwd,vm['moid'])
   except Exception as e:
      resp = 'Stop failed' + str(e)

   assert vm, 'VM info not found'
    
   vmDir = '/vmfs/volumes/%s/%s/' %(vm['datastore'],vmname)

   vmdkFile = vmDir + vmdkFileFormat %vmname
   vmdkFlatFile= vmDir + vmdkFlatFileFormat %vmname
   
   #delete the vmdk file
   try:
      cmd = removeComand%vmdkFile 
      log('Executing command '+ cmd)
      #resp +=
      r = executeCommand(ip,un,pwd,cmd) 
      log(str(r))
      resp +='\nRemoving old file ref : Success'
   except Exception as e:
      resp +='\nRemoving old file ref : Failed, ' + str(e)

   #delete the flat file
   executeCommand(ip,un,pwd,cmd)
   try:
      cmd = removeComand%vmdkFlatFile 
      log('Executing command '+ cmd)
      #resp +=
      r = executeCommand(ip,un,pwd,cmd) 
      log(str(r))
      resp +='\nRemoving old file : Success'
   except Exception as e:
      resp +='\nRemoving old file : Failed, ' + str(e)
    
   eggFilePath = '/vmfs/volumes/DATASTORE02/ISO/vEOS-65.1-disk1.vmdk'

   #extract the file
   try:
      cmd  = vmdkConvertCommandFormat %(eggFilePath,vmdkFile)
      log('Executing command '+ cmd)
      #resp +=
      r = executeCommand(ip,un,pwd,cmd) 
      log(str(r))
      resp +='\nReplacing with new file : Success'
   except Exception as e:
      resp +='\nReplacing with new file, ' + str(e) 

   resp +='\nstarting VM'
   try:
       start(ip,un,pwd,vm['moid'])
   except Exception as e:
      resp = '\nStart failed' + str(e) 
   return resp


def santize(devices,hyperVisorIp,logFile):
   msg = ''
   try: 
      logToFile(logFile,'Reading hypervisior info...')
      hyperVisor = getHyperVisiorByIp(hyperVisorIp)
      logToFile(logFile,'Reading hypervisior info completed')
      #TODO add condition to check the gypervisor
      for device in devices:
         try:
            logToFile(logFile,'Sanitizing device :%s initiated..' %device['name'])
            msg += resetVm(device['name'],hyperVisor)
            logToFile(logFile,msg)
            logToFile(logFile,'Sanitizing device :%s completed' %device['name'])
         except Exception as e: 
            msg +='\nDevice %s failed to sanitize. Cause %s' %(device['name'],str(e))
            logToFile(logFile,msg)
            logToFile(logFile,'Sanitizing device :%s failed' %device['name'])
   except Exception as e:
      msg =  "Error " + str(e)
      logToFile(logFile,msg)
   return msg

def getDHCPLoginInfo(ip):
   condition = 'ip like "%s"' %ip
   data = db.getDataWithCondition('DHCPServers',['username','password','id'],condition)
   assert len(data)==1,'No DHCP info found'
   data = data[0]
   return [data['username'],data['password']]

def saveLog(msg,user,logfile):
   try:
      date = str(datetime.datetime.now())
      db.add('AllocationHistory',{'logdate':date,'user':user,'log':msg,'detailLogFile':logfile}
   except Exception as e:
      log(str(e))
      pass

def readLog(logFile):
   localPath = allocationLogLocation+ logFile
   assert os.path.exists(localPath),'There is no log asssociated for the request ' + str(logFile)
   with open(localPath,'r') as f:
      return {'status':'success','data':f.read()} 

def main():
	form = cgi.FieldStorage()  
	act = form.getvalue('action') 
   
	resp =''
	
	#TODO validate
	if  act == 'getPools':  
		resp = getPools()
	elif  act == 'getPool':  
		uid = form.getvalue('uid') 
		assert uid,'Invalid Pool reference'
		resp = getPoolInfo(uid)
	elif  act == 'savePoolHypervisor':  
		uid = form.getvalue('uid') 
		hypervisor = form.getvalue('hypervisor') 
		assert uid and hypervisor , 'All the fields are required'
		resp = mapHyperisor(uid,hypervisor)
	elif  act == 'savePoolEnv':  
		uid = form.getvalue('uid') 
		assignaction = form.getvalue('assignaction')
		username = form.getvalue('username')
		password = form.getvalue('password')
		assert uid and assignaction,'Bad request'
		assert username and password,'Username and password cannot be null' 
		assert authenticate(username,password), "invalid credentials"
		sanitize = form.getvalue('sanitize')
		serverip = form.getvalue('serverip')
                [dhcpUn,dhcpPwd]  = getDHCPLoginInfo(serverip); 
		if assignaction=='assign':
			environment = form.getvalue('environment')
			numdays = str(form.getvalue('numdays'))
			assert numdays.isdigit(), 'Invalid number of days'
			#log 					
			logFile = str(uuid.uuid4())
			msg =  'Assign initated. Pool id: %s, Server : %s,Envirnment : %s, Sanitize :%s, numdays:%d' %(str(uid),str(serverip),str(environment), str(sanitize),numdays)
			saveLog(msg,username,logFile)
    			thread = Thread(target = assign, args = (uid,sanitize,numdays,serverip,dhcpUn,dhcpPwd,logFile, ))
    			thread.start() 
			resp = {'status':'success','data':'Assign initiated','log':logFile}
		elif assignaction=='release':
			logFile = str(uuid.uuid4())
			msg =  'Release initated. Pool Id : %s, Server :%s, Sanitize :%s' %(str(uid),str(serverip), str(sanitize))
			saveLog(msg,username,logFile)	
    			thread = Thread(target = release, args = (uid,sanitize,serverip,dhcpUn,dhcpPwd,logFile, )) 
			resp = {'status':'success','data':'Release initiated','log':logFile}
		else:
			assert False,'Invalid request'
	elif act == 'showLog':
		logfile = form.getvalue('logfile')
		assert  logfile,'No records'
		resp = readLog(logfile)

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
  


