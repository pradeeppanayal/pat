#!/usr/bin/python2
import sys
import os
import re
import json
import cgi, cgitb 

__author__ ='Pradeep CH'
__version__='1.0.0'


#sys.path.append('../Lib') 
from historyManger import getHistory,readHistory

targetUrl = '#'
def printPage(content):
	#html.printHeader("IP History") 
	#html.printBodyContent(content) 
	print 'Content-type:text/html\r\n\r\n'
	print json.dumps(content)

def main():
	form = cgi.FieldStorage() 
	act = form.getvalue('action')  
	content = ''
	if act=='history':
		content = getFullHistory()
	elif act=='loadhistory':
		fname = form.getvalue('fname')  
		content = {'status':'success','data':readHistory(fname)}
	else:
		content ={'status':'error','data': 'Invalid action'}
	printPage(content)

def getFullHistory(): 
	content =''
	try:
		fullcontent = []
		history = getHistory() 
		if len(history) ==0:
			fullcontent = []
		else:  
			for item in history: 
				ips = item.strip().split(' ') 
				try:
					assert len(ips) ==5, 'Inavlid entry at history tracker'				
					content = {'fileName':ips[0],'startIp':ips[1],'endIp':ips[2],'date':ips[3]+' ' + ips[4]}
					fullcontent.append(content)
				except:
					pass
		fullcontent.reverse()
		content = {'status':'success','data':fullcontent}
	except Exception as e:
		content ={'status':'error','data':'Something went wrong.'}
	return content
if __name__ == "__main__":
	main()
