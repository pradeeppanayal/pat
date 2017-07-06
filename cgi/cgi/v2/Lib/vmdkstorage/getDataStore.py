
"""
Python program for listing the vms on an ESX / vCenter host with datastore
"""
 
import atexit 
import sys
import re

sys.path.append('../../Lib')

from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vim

def getDataStore(serverIp,username,password):
   #connect
   si = SmartConnect(host=serverIp,
                     user=username,
                     pwd=password) 

   if not si:
       assert False,"Could not connect to the specified host using specified username and password" 

   atexit.register(Disconnect, si)

   content = si.RetrieveContent()
   vms = {}
   for child in content.rootFolder.childEntity:
      if hasattr(child, 'vmFolder'):
         datacenter = child
         vmFolder = datacenter.vmFolder
         vmList = vmFolder.childEntity
         for vm in vmList:  
            m = re.search('\[(.*)\]',vm.config.files.vmPathName)
            dataStore = 'No data'
            if m:
               dataStore = m.group(1) 
            mac = getmac(vm)

            if not mac or mac=='':
               continue

            vms[mac] = {'datastore':dataStore,'moid':vm._moId,'mac':mac,'name':vm.name} 
   return vms

def getmac(vm):
   try:
      devices = vm.config.hardware.device
      for device in devices:
         if('Network adapter' not in device.deviceInfo.label):
            continue
         connectStatus = 'Not connected'
         if device.connectable.connected:
            connectStatus = 'Connected'
         return device.macAddress          
   except:
      return 'Error'

if __name__=='__main__':
   print getDataStore('10.10.100.201','root','Payoda#89')
 
