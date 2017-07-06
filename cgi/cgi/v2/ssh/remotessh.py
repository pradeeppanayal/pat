#!/usr/bin/python

# Import modules for CGI handling 
import cgi, cgitb 

import os
import sys
sys.path.append('../Lib')

from htmlutil import html 
from sshclient import SSHClient
#
#Author Pradeep CH
#
__author__ ='Pradeep CH'
__version__='1.0.0'
 

# Create instance of FieldStorage 
form = cgi.FieldStorage() 
clientIp = cgi.escape(os.environ["REMOTE_ADDR"])

bodyContent = ''#html.getBackButton('/pat/ssh/remotessh.htm')

# Get mode from fields 
un = form.getvalue('username')
ip = form.getvalue('ip')

if not ip or not un:
	bodyContent +='IP and Username required.' 
else:
	bodyContent += 'Your machine IP is %s <br>' %(str(clientIp)) 
	try:
		cl = SSHClient(clientIp)
		cl.enableSSH(ip,un)
		bodyContent +='SSH successfull'
	except Exception as e:
		bodyContent += 'Could not connect to remote machine. Make sure the PAT plugin is running in your machine, Cause : %s' %str(e)
#print html
html.printHeader('Authetication Validation')
html.printBodyContent(bodyContent)
