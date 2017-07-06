#!/usr/bin/python

import sys
import re
import json
sys.path.append('../Lib')
from IPAddressManager import parser
from commandexecutor import executeCommand

# Import modules for CGI handling 
import cgi, cgitb   


def executeCommands(ips,cmds,un,pwd): 
   deviceLevelResp = []
   for ip in ips: 
      try:
         tempResp = executeCommand(ip,cmds,un,pwd) 
         deviceLevelResp.append({'status':'success','ip':ip,'data':tempResp})
      except Exception as e:
         deviceLevelResp.append({'status':'error','ip':ip,'data':str(e)}) 
   return {'status':'success','data':deviceLevelResp}

def main():
   # Create instance of FieldStorage 
   form = cgi.FieldStorage() 
   ips = form.getvalue('ips') 
   un =  form.getvalue('username') 
   pwd = form.getvalue('password') 
   cmd = form.getvalue('cmd') 
   if not cmd or not ips:
      resp = {'status':'error','data':'Invalid params'}
   else:      
      cmds= re.split('\n+',str(cmd))
      ips = [ip for ip in parser.parse(ips) if ip.strip()!='']
      if not un or not pwd:
         un = 'cvpuser'
         pwd ='root' 
      resp = executeCommands(ips,cmds,un,pwd)
 
   resp = json.dumps(resp)
   print resp
 
if __name__ == "__main__":
   print "Content-type:text/html\r\n\r\n"
   try:
      main()
   except Exception as e :
      print {'status':'error','data':'Something went wrong. Cause :' + str(e)}
