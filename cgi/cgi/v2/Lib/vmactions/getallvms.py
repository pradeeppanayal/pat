
"""
Python program for listing the vms on an ESX / vCenter host
"""
 
import atexit 
import sys

sys.path.append('../Lib')

from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vim

def getVmInfo(vm, depth=1):
   vms = []
   """
   Print information for a particular virtual machine or recurse into a folder
   or vApp with depth protection
   """
   maxdepth = 10

   # if this is a group it will have children. if it does, recurse into them
   # and then return
   if hasattr(vm, 'childEntity'):
      if depth > maxdepth:
         return
      vmList = vm.childEntity
      for c in vmList:
         vms.extend(c, depth+1)
      return vms

   # if this is a vApp, it likely contains child VMs
   # (vApps can nest vApps, but it is hardly a common usecase, so ignore that)
   if isinstance(vm, vim.VirtualApp):
      vmList = vm.vm
      for c in vmList:
         vms.extend(c, depth+1)
      return vms

   summary = vm.summary
   vm = {'id':vm._moId,'name':summary.config.name,'status':summary.runtime.powerState,'memory':vm.config.hardware.memoryMB,'cpu':vm.config.hardware.numCPU} 

   if summary.guest != None:
      ip = summary.guest.ipAddress
      if ip != None and ip != "":
         vm['ip']=ip
   vms.append(vm) 
   return vms

def getAllVms(serverIp,username,password):
   #connect
   si = SmartConnect(host=serverIp,
                     user=username,
                     pwd=password) 

   if not si:
       assert False,"Could not connect to the specified host using specified username and password" 

   atexit.register(Disconnect, si)

   content = si.RetrieveContent()
   vms = []
   for child in content.rootFolder.childEntity:
      if hasattr(child, 'vmFolder'):
         datacenter = child
         vmFolder = datacenter.vmFolder
         vmList = vmFolder.childEntity
         for vm in vmList:
            vms.extend(getVmInfo(vm))  
   return vms

if __name__=='__main__':
   print getAllVms('10.10.100.201','root','Payoda#89')
 
