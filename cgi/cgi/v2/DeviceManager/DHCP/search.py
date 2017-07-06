#!/usr/bin/python


__author__ ='Pradeep CH'

import sys
import os
from os.path import expanduser 
import json

# Import modules for CGI handling 
import cgi, cgitb 


sys.path.append('../../Lib')
from sqldb import db 


sourcedirectory =  expanduser("~") + "/pat/"
sourceFolder = sourcedirectory+'dhcpconfig/' 
  
def readFile(ip):
   cfileName = sourceFolder +ip+'.conf'
   assert os.path.exists(cfileName),'Configuration file not found. Synch config for dhcp '+ str(ip)  
   with open(cfileName,'r') as f:
      return f.read()

def performSearch(data,keyword):
	if keyword not in data:
		return
	resp =''
	lineNum =0
	lines= data.split('\n')
	for line in lines:
		lineNum +=1
		if keyword in line:
			formatedLine = formatLine(line,keyword)
			resp += '<span class="lineNo">Line %d :</span> %s</br>' %(lineNum,formatedLine)
	return resp

def formatLine(line,searchKey):
   #return line.replace(searchKey,'<span id="highligh" style="font-weight:bold">'+ searchKey+'</span>')
   return line.replace(searchKey,'<span class="highligh">'+ searchKey+'</span>')


def search(keyword):   
   servers =  db.getData('DHCPServers',['id','ip'])
   assert servers,'No DHCP info found'
   wholeData ={}
   ipUid ={}
   bodyContent =''
   for server in servers:
      data = readFile(server['ip'])
      wholeData[server['ip']]= data
      ipUid[server['ip']]= server['id']
   assert len(wholeData)>0,'There is no configuration to perform search'
   matchFound = False
   for ip,data in wholeData.items(): 
      resp = performSearch(data,keyword)
      if resp:
          bodyContent +='<h4> Match found in Server <a target="blank" href="/pat/v2/dhcp/manage.htm?ip=%s&uid=%s"> %s</a></h4>' %(ip,ipUid[ip],ip)
          bodyContent += resp
	  matchFound = True
   if not matchFound:
      bodyContent = '</br>Match not found :('
   return {'status':'success','data':bodyContent}

def main():
   # Create instance of FieldStorage 
   form = cgi.FieldStorage() 

   keyword = form.getvalue('keyword')
   assert keyword and keyword!='','Keyword cannot be empty' 
   resp = search(keyword)
   print json.dumps(resp)

if __name__ == "__main__":
   print 'Content-type:text/html\r\n'
   try:
      main()
   except Exception as e :
      print json.dumps({'status':'error','data':'%s' %str(e)})




	


