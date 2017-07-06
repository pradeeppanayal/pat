#!/usr/bin/python     
__author__ ='Pradeep'




class ServerInfo(object):
   def __init__(self):
      self.id = ''
      self.ip = ''
      self.username = ''
      self.password = ''
      self.identifier = ''
      self.status = 'Not checked'

   def getAttributes(self):
      return {'id':self.id,'ip':self.ip,'username':self.username,'password':self.password,'identifier':self.identifier,'status':self.status}

   def setAttributes(self,a):
      self.id = a['id']
      self.ip =a['ip']
      self.username = a['username']
      self.password = a['password']
      self.identifier = a['identifier']
      self.status = a['status']

class EnvInfo(ServerInfo):
   def __init__(self):
      super(EnvInfo,self).__init__()
      self.bootstrap = ''
      self.description = ''
      self.team = ''
      self.phase = ''

   def getAttributes(self):
      attr = super(EnvInfo,self).getAttributes()
      attr['bootstrap']= self.bootstrap
      attr['description']= self.description
      attr['team']= self.team
      attr['phase']= self.phase
      return attr

   def setAttributes(self,a):
      super(EnvInfo,self).setAttributes(a)   
      self.bootstrap = a['bootstrap']
      self.description = a['description'] 
      self.team = a['team'] 
      self.phase = a['phase'] 

class Hypervisor(ServerInfo):
   def __init__(self):
      super(Hypervisor,self).__init__()
      self.type = ''
   def getAttributes(self):
      attr = super(Hypervisor,self).getAttributes()
      attr['type']= self.type
      return attr

   def setAttributes(self,a):
      super(Hypervisor,self).setAttributes(a)                
      self.type = a['type'] 

class DHCPServer(ServerInfo):
   def __init__(self):
      super(DHCPServer,self).__init__()
      self.configStatus = 'Absolute'
      self.configAvailable ='Not found'
      self.configmd5 = ''
      self.configSynchUp='No info'

   def getAttributes(self):
      attr = super(DHCPServer,self).getAttributes()
      attr['configStatus']= self.configStatus
      attr['configAvailable']= self.configAvailable
      attr['configmd5']= self.configmd5
      attr['configSynchUp'] = self.configSynchUp
      return attr

   def setAttributes(self,a):
      super(DHCPServer,self).setAttributes(a)                
      self.configStatus = a['configStatus']          
      self.configmd5 = a['configmd5']         
      self.configAvailable = a['configAvailable'] 
      self.configSynchUp = a['configSynchUp']


 
