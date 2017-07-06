#!/usr/bin/python2
 
import sys
import os
from os.path import expanduser 
import re
import json
import cgi
import subprocess
sys.path.append('../../Lib')
from ParamikkoUtil import checkAuthentication

def check(ip,un,pwd):
   try:
      DEVNULL = open(os.devnull,'w')
      subprocess.check_call(['ping','-c1',ip],
                                  stdout=DEVNULL) 
   except:
	return {'status':'success','data':'Not Reachable'}
   if not checkAuthentication(ip,un,pwd):
	return {'status':'success','data':'Authentication Failure'}

   return {'status':'success','data':'Online'}

def main():
	form = cgi.FieldStorage() 
	act = form.getvalue('action') 
	 
	resp =''
 
	if  act == 'statusServer':
		un = form.getvalue('uname') 
		ip = form.getvalue('ip') 
		pwd = form.getvalue('pwd') 
		assert un and pwd and ip, 'Provide IP Username and Password' 
		resp=check(ip,un,pwd)
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
  


