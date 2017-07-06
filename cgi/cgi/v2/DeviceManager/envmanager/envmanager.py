#!/usr/bin/python2
 
import sys
import os
from os.path import expanduser 
import re
import json

sys.path.append('../../Lib')

from commonutil import getRandomId 
from beans import EnvInfo
from sqldb import db

import cgi, cgitb 

__author__ ='Pradeep CH'
__version__='1.0.0'
 

targetName = 'EnvInfo'

def addServer(s):
    try:
        #addEntry(self,mapper,tablename)
       db.addEntry(s.getAttributes(),targetName)
       return {'status':'success','data':'Environment added successfully'}

    except Exception as e:
       return {'status':'error','data':str(e)}


def updateServer(s,key,keyidentifier):
    try:
        #updateEntry(self,mapper,tablename,key,keyidentifier):
       db.updateEntry(s.getAttributes(),targetName,key,'id')
       return {'status':'success','data':'Environment updated successfully'}
    except Exception as e:
       return {'status':'error','data':str(e)}

def getAllServers():
    try: 
       s = EnvInfo()
       #def getData(self,tablename,keyset,key=None,keyidentifier = ''):
       data =  db.getData(targetName,s.getAttributes().keys())
       return {'status':'success','data':data}
    except Exception as e:
       return {'status':'error','data':str(e)}

def getServerInfo(uid):
    try: 
       s = EnvInfo()
       #def getData(self,tablename,keyset,key=None,keyidentifier = ''):
       data =  db.getData(targetName,s.getAttributes().keys(),uid,'id')
       assert len(data)==1,'No info'
       data = data[0]
       return {'status':'success','data':data}
    except Exception as e:
       return {'status':'error','data':str(e)}

def main():
	form = cgi.FieldStorage() 
	act = form.getvalue('action') 
	
	s = EnvInfo()
	s.id = form.getvalue('uid')
	s.ip = form.getvalue('ip')
	s.username = form.getvalue('uname')
	s.password =form.getvalue('pwd')
	s.bootstrap =form.getvalue('bootstrap')
	s.team =form.getvalue('team') 
	s.phase =form.getvalue('phase') 
	s.description =form.getvalue('desc') 
	s.status =form.getvalue('status') 
	s.identifier =form.getvalue('identifier') 

	resp =''
	
	#TODO validate
	if  act == 'addserver':
		assert s.ip and s.username and s.password and s.identifier and s.bootstrap and s.phase and s.team and s.description,'Invalid data. All the fields are required'	
		s.id= getRandomId()
		resp = addServer(s)
	elif act =='updateserver':
		assert s.ip and s.username and s.password and s.bootstrap and s.identifier and s.phase and s.team and s.description,'Invalid data. All the fields are required'
		assert s.id, 'Invalid id'
		resp = updateServer(s,s.id,'id')
	elif act == 'loadservers':
		resp = getAllServers()
        elif act == 'loadServer':
		resp = getServerInfo(s.id)
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
  


