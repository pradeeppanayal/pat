#!/usr/bin/python2

import multiprocessing
import subprocess
import sys
import os
sys.path.append('../Lib')

from htmlutil import html
from historyManger import saveHistory
from IPAddressManager import parser
# Import modules for CGI handling 
import cgi, cgitb 

__author__ ='Pradeep CH'
__version__='1.0.0'



def printPage(content):
	html.printHeader("IP Sweep") 
	html.printBodyContent(content) 

def pinger( job_q, results_q ):
    DEVNULL = open(os.devnull,'w')
    while True:
        ip = job_q.get()
        if ip is None: break

        try:
            subprocess.check_call(['ping','-c1',ip],
                                  stdout=DEVNULL)
            results_q.put(ip)
        except:
            pass

def log(msg='',breakReq=True):
    msg.replace(' ','&nbsp;')
    if breakReq:
        msg += '</br>'
    print msg

def main(ips):

    ips =parser.parse(ips)
    aips = []

    assert ips, 'No ips to be validated'
        
    total = len(ips)
    
    pool_size = 20
    
    assert total > 0, 'No ips to be validated' 

    jobs = multiprocessing.Queue()
    results = multiprocessing.Queue()

    pool = [ multiprocessing.Process(target=pinger, args=(jobs,results))
             for i in range(pool_size) ]

    for p in pool:
        p.start()

    for ip in ips:
        jobs.put(ip)

    for p in pool:
        jobs.put(None)

    for p in pool:
        p.join()

    success=0

    if results:
        success = results.qsize()
    content =''
    #summary
    #content +='Start IP : %s' %ipstart
    #content += 'Last IP : %s ' %ipend

    content +='Total IPs validated : %d ' %total
    content +='</br>' 
    content +='Active IPs count : %d' %success
    content +='</br>' 
    content +='Inactive IPs : %d' %(total-success) 

    while not results.empty():
       	ip = results.get()
        aips.append(ip)

    inactiveIps=[ i for i in ips if i not in aips]

    #log('Inactive IPS :')
    #log(str(aips))
    
    #log('Inalive IPS :')
    #log(str(inactiveIps))
    aips.sort()
    inactiveIps.sort()

 
    content +='<h4>Active IPs</h4>' 
    content +='</br>'.join(aips) 
    content +='<h4>Inactive IPs</h4>'
    content +='</br>'.join(inactiveIps) 
    try: 
	ipstart= ips[0]
	ipend =ips[len(ips)-1] 
        saveHistory(content,ipstart,ipend)
    except Exception as e:
	content += str(e)
	pass
    printPage(content)
# Create instance of FieldStorage 
form = cgi.FieldStorage() 

# Get mode from fields  
ips = form.getvalue('ips')  
if not ips:
	endip =form.getvalue('endip')  
	startip =form.getvalue('startip')  
	if endip and startip:
		ips = startip +'-'+endip
try:
    main(ips) 
except Exception as e:
    printPage('Exception '+str(e))


