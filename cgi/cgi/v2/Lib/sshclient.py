#!/usr/bin/python           
import socket       
__author__ ='Pradeep'

class SSHClient(object):
	def __init__(self,host,port=1243):
		self.host= host
		self.port = port
	
	def enableSSH(self,targetIP,targetUsername): 
		cmd  ='ssh %s@%s' %(targetUsername,targetIP)
		self.executeCommand(cmd)  

	def executeCommand(self,cmd):
		try: 
			s = socket.socket()
			s.connect((self.host, self.port))
			s.send(cmd)
			resp = s.recv(1024)
			if resp != 'Received':
				raise Exception('Remote SSH Unsuccessfull')
			s.close()      
		except Exception as e:
			raise Exception(str(e))

if __name__ == "__main__":
	cl = SSHClient('192.168.5.9')
	print cl.enableSSH('192.168.5.9','pradeep.k')
