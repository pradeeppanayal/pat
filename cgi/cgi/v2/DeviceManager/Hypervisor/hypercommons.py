
import sys
sys.path.append('../../Lib')

from beans import Hypervisor
from sqldb import db

def getServerInfoById(uid): 
   s = Hypervisor()
   #def getData(self,tablename,keyset,key=None,keyidentifier = ''):
   data =  db.getData('Hypervisors',s.getAttributes().keys(),uid,'id')
   assert len(data)==1,'No info'
   data = data[0]
   return data 
