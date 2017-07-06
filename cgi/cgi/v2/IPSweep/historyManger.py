#!/usr/bin/python2

import sys

import os.path
import os
import datetime
from os.path import expanduser 

sys.path.append('../Lib')
from commonutil import getRandomId
from htmlutil import html 


sourcedirectory =  expanduser("~") + "/pat/"
sourceFolder = sourcedirectory +'/sweephistory'

fileFormat= '%s/%s'
source = fileFormat %(sourceFolder,'files')
maxRec =10

#create the folder structure
if not os.path.exists(sourceFolder):
	os.makedirs(sourceFolder)
	open(source,'w')

def getHistory():
	if not os.path.exists(source):
		return []

	with open(source,'r') as f:
		data = f.read()
		if not data or data.strip()=='':
			return []
		return data.split('\n')  

def writeData(filename,data):
	with open(filename,'w') as f:
		f.write(data)

def updateHistory(fileNames):
	with open(source,'w') as f:
		f.write('\n'.join(fileNames))

#This changes the data to complete html 
def formatData(data,startIP,endIP,reg_format_date):
	if data:
		title = 'Sweep History:%s-%s' %(startIP,endIP)		
		prefix =''
		#prefix ='Content-type:text/html\r\n\r\n'
		prefix +='<html><head><title>%s</title></head></body>' %title
		prefix +='<h3>Sweep History </h3>'
		prefix +='Date :%s</br>' %(reg_format_date) 
		prefix +='Range :%s&nbsp;-&nbsp;%s</br></br>' %(startIP,endIP)
		
		data =prefix + data
		data +='</body></html>'
		return data
	return 'No data'

def readHistory(fname):
	fullname = fileFormat %(sourceFolder,fname)
	if os.path.isfile(fullname):
		with open(fullname) as f:
			return f.read()
	return 'No data to be shown'

def saveHistory(data,startIp,endIP):
	global maxRec
	d_date = datetime.datetime.now()

	fileName = getRandomId() +'.htm'

	reg_format_date = d_date.strftime("%Y-%m-%d %H:%M:%S")

	filePath = fileFormat %(sourceFolder,fileName)

	historyentry = '%s %s %s %s' %(fileName,startIp,endIP,reg_format_date)	
	
	existingFileNames = getHistory()

	if len(existingFileNames)>=maxRec:
		lastEntry = existingFileNames[maxRec-1]
		os.remove(fileFormat %(sourceFolder,lastEntry.split(' ')[0]))
		existingFileNames.remove(existingFileNames[maxRec-1])
	
	data = formatData(data,startIp,endIP,reg_format_date)
	writeData(filePath,data)
	existingFileNames.reverse()
	existingFileNames.append(historyentry)
	updateHistory(existingFileNames)
		
