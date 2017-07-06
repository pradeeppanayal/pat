#!/usr/bin/python

# Import modules for CGI handling 
import cgi, cgitb 

import time
import re
from Reload import ReloadDevices
from htmlutil import html 
import sys
import os
sys.path.append('../Lib')
from IPAddressManager import parser
#
#Author Pradeep CH
#
__author__ ='Pradeep CH'
__version__='1.0.0'


def restartSingleDevice(ip,un,pwd):
	deviceLoader = ReloadDevices()
	try: 
		if un and pwd:
			return deviceLoader.realoadDevice(ip,un,pwd)
		else:
			return deviceLoader.realoadDevice(ip) 
	except Exception as e:
		return str(e)

		
def log(msg):
	print msg+'<br/>'

def restartMultiple(ips,un,pwd):
	resp =''
	for ip in ips:
		ip = ip.strip()
		if ip == '':
			continue;
		#log('IP %s is trying to reset ' %ip)
		stat = restartSingleDevice(ip,un,pwd);
		#stat ='Success'
		#log('Restring IP %s completed with status %s' %(ip,stat))
		resp +='<br />' + 'IP %s : %s' %(ip,str(stat))
	return resp

# Create instance of FieldStorage 
form = cgi.FieldStorage() 


bodyContent = '' #html.getBackButton('/pat/DeviceManager/manager.htm')

# Get mode from fields
#mode= form.getvalue('mode')

un = form.getvalue('username')
pwd = form.getvalue('pwd')
ips =  form.getvalue('ips')
if not ips:
	bodyContent +='No IPs provided'
else:
	try: 
		mips = parser.parse(ips)  
		bodyContent +=restartMultiple(mips,un,pwd)		
	except Exception as e:
		bodyContent +='Excption : %s' %str(e)
#print html
html.printHeader('Device Reset')
html.printBodyContent(bodyContent)
