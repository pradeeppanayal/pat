#!/usr/bin/python


__author__ ='Pradeep CH'

import sys
import os 
import json
import cgi
 
def download(fileName,data):	
	try:
		downloadFileName = fileName 
		print 'Content-Disposition: attachment; filename="%s"' % downloadFileName
		#print "Content-Length: " + str(os.stat(fullPath).st_size)
		print    # empty line between headers and body
		print data

	except Exception as e:
		print "Content-type:text/html\r\n\r\n"
		print 'Unexpected error occured. %s' %str(e)

	
#
dhcpServerResourceFile = '../../../DHCPServers/servers'

def loadAllServers():
	data =""
	with open(dhcpServerResourceFile,'r') as f:
		data = f.read()
	servers = {}
	if data:
		servers = json.loads(data)
	return servers

def getServerInfo(ip):
	servers = loadAllServers()
	serverInfo ='No data found'
	for server in servers:
		if server['ip']==ip:
			serverInfo = json.dumps(server)
	print "Content-type:text/html\r\n\r\n"
	print serverInfo

form = cgi.FieldStorage() 

action = form.getvalue('action')

if action == 'download':
	data = form.getvalue('data')
	fileName = form.getvalue('fileName')
	download(fileName,data);
elif action=='dhcpserverInfo':
	ip =  form.getvalue('ip')
	getServerInfo(ip);

else:
	print "Content-type:text/html\r\n\r\n"
	print 'Invalid action'
