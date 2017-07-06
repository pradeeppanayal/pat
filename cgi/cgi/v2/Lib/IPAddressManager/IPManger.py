#!/usr/bin/python           
import socket    
import re   
__author__ ='Pradeep'

class  IPAdressParcer(object):
	def parse(self,data):
		ips = []
		lines = re.split('[\n\s;,]+',data) 
		for line in lines:
			if '-' in line:
				temp = line.split('-')
				assert len(temp)==2, 'Invalid range : %s' %line
				ips.extend(self.getRange(temp[0],temp[1]))
			else:
				ips.append(line)
		return ips

	def getRange(self,ipstart,ipend):
		ips =[]
		try:
			s = [int(numeric_string) for numeric_string in ipstart.split('.')]
			e = [int(numeric_string) for numeric_string in ipend.split('.')]
		except Exception as e:
			assert False, 'Invalid IP range'
	
		assert  len(s)==4 and len(e)==4, 'Invalid IP Address.'
 
		while not (e[0]==s[0] and e[1]==s[1] and e[2]==s[2] and e[3]<s[3]):
		
			ip =  '%d.%d.%d.%d'%(s[0],s[1],s[2],s[3])
			ips.append(ip)
			#move to the next
			s[3] +=1		
			if s[3]==255:
				s[2] +=1
				s[3] =1
			if s[2]==255:
				s[1] +=1
				s[2] =1
			if s[1]==255:
				s[0] +=1
				s[1] =1
			if s[0] >255 :
				break;
		return ips 
