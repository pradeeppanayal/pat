# start by importing the library


import sys
sys.path.append('../Lib')

from commandexecutor import validateAuthentication
from commandexecutor import executeCommand

import pyeapi 
import re

__author__ ='Pradeep CH'
__version__='1.0.0'

'''
This class contains list methods that allows to restart devices
'''
class ReloadDevices(object):
	def realoadDevice(self,ip,userName='cvpuser',pwd='root'):
		#self.log('Trying to Reset %s' %(ip)) 
		try:
			#self.log('Trying to connect to device')
			validateAuthentication(ip,userName,pwd)
		except Exception as e:
			#self.log( 'Authetication failed' )
			return 'Authentication failure'
		
		try:
			#self.log('Deleteting startup config')
			executeCommand(ip,['enable','delete flash:startup-config'],userName,pwd)
			#self.log( 'Startup config deleted')
		except Exception as inst:
			#self.log( 'Satrtup config not deleted: '+str(inst) ) 
			pass
		try:
			#self.log( 'Deleteting zerotouch-config')
			executeCommand(ip,['enable','delete flash:zerotouch-config'],userName,pwd)
			#self.log( 'zerotouch-config deleted' )
		except Exception as inst:
			#self.log( 'Satrtup config not deleted: '+str(inst)) 
			pass
		try:
			#self.log( 'realoding device')
			executeCommand(ip,['enable','reload now'],userName,pwd)
			#self.log( 'Device Reset triggered')
		except Exception as inst:
			#self.log('Device restart triggered : '+str(inst))
			pass

		#self.log('%s Reset request completed with status %d' %(ip, status),True)
		return 'Device Reset Process Initated..'

	def writeToFile(self,msg):
		with open('result','a') as f:
			f.write('\n' + msg)	
	def reloadDevicesFromFile(self,path):
		data =''

		splitRegEx = '[\s\n,]';
		ipRegEx =  '^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$'

		with open(path,'r') as f:	
			data = f.read();

		ips = re.split(splitRegEx,data)
		#self.log('Extracted IPs :'+ str(ips))
		
		self.log('Enetr the credential \n')
		envUsername = self.readInput('Username :')
		envPassword = self.readInput('Password :')
 
		for ip in ips:

			if re.match(ipRegEx,ip) ==None :
				self.log('Invalid IP. IP %s skipped' %str(ip))
				continue

			if self.realoadDevice(ip,envUsername,envPassword) != 1:
				self.log('Reset failed')	
	 
	def getEnvPassword(self):
		uname = self.readInput('Enter the enviornment details. This will be used if the default username and password fails to authenticate \nUsername :');
		pwd = self.readInput('Password :');
		return [uname,pwd]

	def readInput(self,msg):
		return raw_input(msg)

	def log(self,msg,writeToFile=False):
		print msg+'<br/>'
		if writeToFile:
			self.writeToFile(msg)

def main():
	deviceLoader = ReloadDevices()
	ch = 0
	while ch !=4:

		menu = '1. Reset a single device'
		menu = menu + '\n2. Reset devices from a file'
		menu = menu + '\n3. Reset devices from DHCP config'
		menu = menu + '\n4. Exit'
		menu = menu + '\nEnter your choice [1-4]:'

		ch = int(deviceLoader.readInput(menu))

		if ch == 1:
			ip = deviceLoader.readInput('Enter IP :')
			if deviceLoader.realoadDevice(ip)!= 1:
				retry = 'Reset failed try with another credentials (y/n):'
				while deviceLoader.readInput(retry) == 'y':
					#get the input
					uname = deviceLoader.readInput('Username :')
					pwd = deviceLoader.readInput('Password :')
					
					if deviceLoader.realoadDevice(ip,uname,pwd)== 1:
						break;
					else:
						deviceLoader.log('Reset failed.')
		elif ch==2:
			fileName = deviceLoader.readInput('Enter the file path :')
			deviceLoader.reloadDevicesFromFile(fileName)
		 
			
if __name__ == "__main__":
	main()
