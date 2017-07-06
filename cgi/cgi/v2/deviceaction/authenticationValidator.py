
import sys

#Add path 
sys.path.append('../Lib') 
from IPAddressManager import parser
from commandexecutor import validateAuthentication

from htmlutil import html 

# Import modules for CGI handling 
import cgi, cgitb 
import re
import json

	
# Create instance of FieldStorage 
form = cgi.FieldStorage() 

#header


# Get mode from fields 
 
ips =  form.getvalue('ips') 
un =  form.getvalue('username') 
pwd =  form.getvalue('pwd')   

bodyContent ='' 

successIPS =[]
failedIPS = []
failedIPSWithCause =[]
total =0

if not ips:
	 bodyContent +='IP address required' 
else:
	if not un or not pwd:
		un ='cvpuser'
		pwd='root'
		bodyContent +='Password not provided. Using default username and password.'
 	try:
		ips = parser.parse(ips)
	except Exception as e:
		bodyContent +='<br><b>Invalid IP address range</b>'
		ips=[]
	for ip in ips:  
		if ip.strip() =='':
			continue
		total +=1
		resp =''
		try:
			validateAuthentication(ip,un,pwd)
			successIPS.append(ip)
		except Exception as e:
			failedIPSWithCause.append('%s     Cause : %s' %(ip,str(e))) 
			failedIPS.append(ip) 
 	#style
	bodyContent +='''<link  rel="stylesheet" href="/pat/v2/style/style.css">
		<link  rel="stylesheet" href="/pat/v2/style/bootstrap.min.css"> '''
	bodyContent +='<h3>Summary</h3>'
	bodyContent +='Total :%d</br>' %total 
	bodyContent +='Success :%d</br>' %len( successIPS)
	bodyContent +='Failed :%d</br>' %len( failedIPS) 
	bodyContent +='</br>'

	bodyContent +='<h3>Success IPs </h3>'
	bodyContent +='<br>Username : %s' %un
	bodyContent +='<br>Password : %s </br>' %pwd
	bodyContent +='<br>'.join(successIPS)
	bodyContent +='</br>'
	bodyContent +='</br>'

	if len(failedIPS)>0:
		bodyContent +='<h3>Failed IPS with Cause</h3>'
		bodyContent +='<br>'.join(failedIPSWithCause) 
		bodyContent +='</br>'

		bodyContent +='<h4>Failed IPs</h4>'
		bodyContent +='<form action="/pat/cgi-bin/v2/deviceaction/authenticationValidator.py" method="post" target="_blank">'
		bodyContent +='<label >%s</label>' %', '.join(failedIPS) 
		bodyContent += '<input type="hidden" name="ips" value="%s"/>' %','.join(failedIPS) 
		bodyContent +='''
			<h4>Try with different credential</h4>
			<table>			 
				<tr>
					<td>Username :</td>
					<td><input type="text" name="username" /> </td>
					<td>Required</td>
				</tr>
				<tr>
					<td>Password :</td>
					<td><input type="password" name="pwd" /> </td>
					<td>Required</td>
				</tr>
			</table>
			</br>  
			<input type="submit" value="Authenticate" />
               		<input type="reset"  />
			'''

html.printHeader('Authetication Validation')

html.printBodyContent(bodyContent)

 
