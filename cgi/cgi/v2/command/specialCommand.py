#!/usr/bin/python
 
import sys
sys.path.append('../Lib')

from commandexecutor import executeCommand


# Import modules for CGI handling 
import cgi, cgitb 
import re
import json

def log(msg,formatSpace=True):
	if formatSpace:
		msg= str(msg).replace(' ','&nbsp;')
	print msg+'<br/>'

def getTheFieldValue(keys,resp): 
	jsonObj = None
	try:
		jsonObj = json.loads(resp)
	except Exception as e :
		return 'Invalid resp from device. Cause : %s. Response : %s' %(str(e),str(resp))
	jsonObj = jsonObj["result"]
 
	
	for item in jsonObj:
		try:
			for key in keys:
				if key not in item.keys():
					raise Exception ('Key %s not found' %key )
				item = item[key]
				resp = item
		except Exception as e:
			resp ='Exception : %s' %(str(e))
	if not resp:
		resp =str(jsonObj)	
	return resp
	
# Create instance of FieldStorage 
form = cgi.FieldStorage() 

#header
print "Content-type:text/html\r\n\r\n"
print "<html>"
print "<head>"
print "<title>Hello - Second CGI Program</title>"
print "</head>"
print "<body>"
print "<a href='/pat/command/specialcommand.htm' style='color:blue'>Go back</a></br></br>"


# Get mode from fields 
 
ips =  form.getvalue('ips') 
un =  form.getvalue('uname') 
pwd =  form.getvalue('password') 
cmd =  form.getvalue('cmd') 
filterDb = form.getvalue('filter') 
jsonKeys=None

if filterDb:
	jsonKeys = filterDb.split(' ')

cmds=[]
 
if not ips:
	log('IP address required')
elif not cmd:
	log('There is no command to execute')
else:
	cmds= cmd.split('\n') 
	ips = re.split('[\n ,;]*',ips)
	
	if un and ips and pwd:
		
		for ip in ips: 
			#log('Executing command on device %s ' %ip)
			try:
				resp = executeCommand(ip,cmds,un,pwd)

				if jsonKeys:
					resp = getTheFieldValue(jsonKeys,resp)

			except Exception as e:
				resp = 'Failed to execute command at device %s, reson: %s' %(ip,str(e))
			
			log('%s\t\t%s' %(ip,str(resp)),False)
			#log('Executing command on device %s completed' %ip)
	else:		
		for ip in ips: 
			#log('Executing command on device %s ' %ip)
			try:
				resp = executeCommand(ip,cmds)

				if jsonKeys:
					resp = getTheFieldValue(jsonKeys,resp)

			except Exception as e:
				resp = 'Failed to execute command at device %s, reson: %s' %(ip,str(e))
			
			log('%s\t\t%s' %(ip,str(resp)),False)
			#log('Executing command on device %s completed' %ip)
	

#Footer
print "</body>"
print "</html>"
