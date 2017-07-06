
__author__='Pradeep CH'
__version__ ='1.0.0'
__date__= '29- Mar- 2017'


import os
import json

from os.path import expanduser 
from getDataStore import getDataStore

sourcedirectory =  expanduser("~") + "/pat/"
vmdkFileRef = sourcedirectory +'vmdkmapper.db'
vmInfoDirectory  = sourcedirectory + 'vminfo/'
vmdkSourceFolder = sourcedirectory + 'vmdks/'

targetPath = '/vmfs/volumes/%s/%s/'

def getDestinationPath(ip,un,pwd,vmname):

   if not os.path.exists(vmInfoDirectory):
      os.makedirs(vmInfoDirectory)
   data = readVmsInfo(ip,un,pwd)
   datastore = '' 
   for key in  data:
      if data[key]['name'] == vmname:
         datastore = data[key]['datastore']
   assert datastore!='', 'No info found'
   return targetPath%(datastore,vmname)

def readVmsInfo(ip,un,pwd,forceSynch=False):
   fname = vmInfoDirectory + ip+'vms.db'
   if not os.path.isfile(fname) or forceSynch:
      synchVM(ip,un,pwd)
   with open(fname,'r') as f:
      data = f.read()
      assert not data or data !='','VM Mapper not found' 
      data = json.loads(data)
      return data

def synchVM(ip,un,pwd):
   fname = vmInfoDirectory + ip+'vms.db'

   data =getDataStore(ip,un,pwd)
   data = json.dumps(data)
   with open(fname,'w') as f:
      f.write(data)

def getVMDKFileLocation(ip,vmname):
   with open(vmdkFileRef,'r') as f:
      data = f.read()
      data = json.loads(data)

      if ip in data.keys():
         data = data[ip]
      else:
         data = data['default']

      source = data ['source']
      loc = ''
      if vmname in data.keys():
         loc = data[vmname]
      else:
         loc = data['default'] 
      if source=='local':
         loc = vmdkSourceFolder+loc
      return [loc,source]

def getVMBaseInfo(ip,un,pwd,forceSynch):
   return readVmsInfo(ip,un,pwd,forceSynch)


def getVMDKInfo(ip,un,pwd,vmname):   
   destPath = getDestinationPath(ip,un,pwd,vmname)  
   [loc,source] = getVMDKFileLocation(ip,vmname)
   return {'destPath':destPath,'source':source,'sourceFilePath':loc}
    


