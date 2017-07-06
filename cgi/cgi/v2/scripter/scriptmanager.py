#!/usr/bin/python2
 
import sys
import os
from os.path import expanduser 
import re
import json
import datetime
sys.path.append('../Lib')
 
from sqldb import db
from beans import EnvInfo
from ParamikkoUtil import checkAuthentication,executeCommand,copyToRemote
from usermanager import authenticate
import cgi, cgitb 


sourcedirectory =  expanduser("~") + "/pat/"
scriptDir = sourcedirectory +'scripts/'


def getScripts(): 
   #def getData(self,tablename,keyset,key=None,keyidentifier = ''):
   try:
      data = db.getData('ScriptMapper',['id','fileName','uploadedBy','uploadedOn','param']) 
      return {'status':'success','data':data}
   except Exception as e:
      return {'status':'error','data':'Unexpected excpetion'}

def uploadFile(data,fileName): 
   fullPath  = scriptDir+ fileName
   assert not os.path.exists(fullPath), 'Duplicate script'
   with open(fullPath,'wb') as f:
      f.write(data)

def saveScriptInfo(filename,uploadedBy,param,scriptType):
   uploadedOn = str(datetime.datetime.now().date())
   db.addEntry({'fileName':filename,'uploadedBy':uploadedBy,'uploadedOn':uploadedOn,'param':param,'scriptType':scriptType},'ScriptMapper')

def getScriptInfo(scriptId):
   data =  db.getData('ScriptMapper',['id','fileName','uploadedBy','uploadedOn','param'],scriptId,'id')
   assert len(data)==1,'No info'
   return data[0]

def execute(scriptid,ip,username,password,arg):
   sinfo = getScriptInfo(scriptid) 
   #Authenticate
   assert checkAuthentication(ip,username,password),'Authentication failure'
   #copy to remote
   remotePath = '/tmp/' + sinfo['fileName']
   sourceFile = scriptDir + sinfo['fileName']
   try:
      copyToRemote(ip,username,password,sourceFile,remotePath)
   except Exception as e:
      assert False,'Script execution on remote machine failed. Cause :' + str(e)
   permissionSetCommand = 'chmod 777 ' + remotePath
   exeCommand = remotePath+' ' + arg
   removeCommand = 'rm -rf ' + remotePath
   executeCommand(ip,username,password,permissionSetCommand)
   resp = executeCommand(ip,username,password,exeCommand)
   executeCommand(ip,username,password,removeCommand)
   return {'status':'success','data':'%s' %resp}

def getScriptInfoResponse(sid):
   sinfo = getScriptInfo(sid) 
   return {'status':'success','data':sinfo}

def main():
   form = cgi.FieldStorage()  
   act = form.getvalue('action') 
   resp =''
	 
   if  act == 'getScripts':  
      resp = getScripts() 
   elif act=='upload':
      fileName =  form.getvalue('scriptname') 
      username =  form.getvalue('username') 
      password =  form.getvalue('password') 
      scriptType =  form.getvalue('scriptType') 
      param =  form.getvalue('param') 
      uploadedFile =  form['script']
      assert fileName and username and password and scriptType, 'All the fields are mandotory'
      assert authenticate(username,password),'Invalid authetication info'
      uploadFile(uploadedFile.file.read(),fileName)
      saveScriptInfo(fileName,username,param,scriptType)
      resp = {'status':'success','data':'Script upload successfull'}
   elif act == 'execute':
      ip = form.getvalue('ip') 
      username =  form.getvalue('username') 
      password =  form.getvalue('password') 
      scriptid =  form.getvalue('id') 
      arg =  form.getvalue('arg') 
      assert ip and username and password and scriptid and arg, 'All the fields are mandotory'
      resp = execute(scriptid,ip,username,password,arg)
   elif act == 'getScriptInfo':
      sid = form.getvalue('id')  
      assert sid , 'Invalid script identifier'
      resp = getScriptInfoResponse(sid)
   else:
      assert False, 'Invalid action'

   print json.dumps(resp)

if __name__ == "__main__":
   print 'Content-type:text/html\r\n'
   try:
      main()
   except Exception as e :
      print json.dumps({'status':'error','data':'%s' %str(e)})
  
