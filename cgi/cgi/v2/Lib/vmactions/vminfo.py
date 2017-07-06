#!/usr/bin/env python
 
""" 
"""

import atexit  
import sys
import re

sys.path.append('../')

from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vim, vmodl

def getDataStore(path):
   try:
      return re.match('.*\[(.*)\].*',path).group(1)
   except:
       return ''
def getVMInfo(ip,un,pwd,dname):
   si = SmartConnect(host=ip,
                     user=un,
                     pwd=pwd)
   assert si, "Cannot connect to specified host using specified username and password"
   
   info = []
   content = si.content
   objView = content.viewManager.CreateContainerView(content.rootFolder,
                                                    [vim.VirtualMachine],
                                                    True)
   vmList = objView.view 
   objView.Destroy()

   vm = [vm for vm in vmList if vm.name == dname]
   assert len(vm) ==1,"Device info not found in the server"
   vm = vm[0]   
   moid = vm._moId
   datastore = getDataStore( vm.summary.config.vmPathName)
   return {'moid':moid,'datastore':datastore} 

if __name__=='__main__':
   print getVMInfo("10.10.100.201",'root','Payoda#89','vEOS-65.91')
