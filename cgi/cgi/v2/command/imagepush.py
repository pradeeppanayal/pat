#!/usr/bin/python
 
import sys
# Import modules for CGI handling 
import cgi, cgitb 
import re
import json
import os

sys.path.append('../Lib')
from commandexecutor import executeCommand
from commandexecutor import validateAuthentication
from IPAddressManager import parser


tempLoc = '../../../../v2/eosimages'
cmds =['enable','configure','install source %s now','reload now']
writeCmd =['enable','write']

HTTP_HOST = os.environ["HTTP_HOST"] 


def executeImagePush(ips,un,pwd,cmds): 
   if not un or not pwd:
      un ='cvpuser'
      pwd= 'root'
   deviceResp = {}
   for ip in ips:
      deviceResp[ip]= ''
      #step 1
      try: 
         validateAuthentication(ip,un,pwd)
         deviceResp[ip] +='Authetication Status:Success'
      except Exception as e: 
         deviceResp[ip] +='Authetication Status:Failed'
         continue
      #step 2
      try: 
         executeCommand(ip,writeCmd,un,pwd) 
         deviceResp[ip] +='\nWrite Status:Success'
      except Exception as e: 
         deviceResp[ip] +='\nWrite Status:Failed' 
      #step 3     
      try:
         deviceResp[ip]  = '\nRestart Response ' + str(executeCommand(ip,cmds,un,pwd) ) 
      except Exception as e:				
         if str(e) == 'unable to connect to eAPI':
            deviceResp[ip]  += '\nImage push to device %s is completed. Restart in progress...' %ip
         else:
            deviceResp[ip]  += '\nImage push to device %s is failed. Reason :%s' %(ip,str(e))

   return {'status':'success','data':deviceResp}

def storeFile(fileName,data):
   with open(fileName,'wb') as f:
      f.write(data)

def formatCmd(cmds,fileName,cgipath):
   #downloadUrl = 'http://'+HTTP_HOST+cgipath +'command/downloadimage.py?fname='+fileName
   downloadUrl = 'http://'+HTTP_HOST+'/pat/v2/eosimages/'+fileName
   cmds[2] = cmds[2] %downloadUrl
   return cmds

def main():
   global cmds
   # Create instance of FieldStorage 
   form = cgi.FieldStorage()
   uploadedFile = form['imgFile']  
   #assert uploadedFile,'No image file uploaded'
   fileName = uploadedFile.filename 
   assert fileName, 'Invalid file name'
   ips =  form.getvalue('ips') 
   un =  form.getvalue('uname') 
   pwd =  form.getvalue('password') 
   save =  form.getvalue('save')  
   cgipath =  form.getvalue('cgipath')  
   destPath = tempLoc+'/'+fileName
   assert ips and cgipath, 'Invalid Param'
   ips = [ip for ip in parser.parse(ips) if ip.strip()!='']
   assert len(ips)>0,'No Ip Address'

   ucmds = formatCmd(cmds,fileName,cgipath)
   storeFile(destPath,uploadedFile.file.read())
   try:
      resp = executeImagePush(ips,un,pwd,ucmds) 
   except Exception as e:
      resp ={'status':'errror','data':str(e)}
   finally:
      try:
         os.remove(destPath) 
      except:
         pass
   resp = json.dumps(resp)
   print resp
 
if __name__ == "__main__":      
   print "Content-type:text/html\r\n\r\n"
   global tempLoc
   try: 
      #create the folder structure
      if not os.path.exists(tempLoc):
         os.makedirs(tempLoc)
      main()
   except Exception as e :
      print {'status':'error','data':'Something went wrong. Cause :' + str(e)}
