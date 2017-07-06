
import paramiko
import uuid
import os

def copyRemoteFile(ip,username,password,remotepath,localfileName):
	#print 'Copying file from %s to local' %(ip) 
	ssh = getSSHClient(ip,username,password)
	ftp = ssh.open_sftp()
	ftp.get( remotepath,localfileName)
	ftp.close()

def getSSHClient(ip,un,pwd):
	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh.connect(ip, username=un,password=pwd,timeout=10)
	return ssh

def checkAuthentication(ip,username,password): 
	try:
		ssh = getSSHClient(ip,username,password) 
		return True
	except paramiko.AuthenticationException as e:
		return False 

def executeCommand(ip,username,password,cmd):
	ssh = getSSHClient(ip,username,password) 
	stdin, stdout, stderr = ssh.exec_command(cmd)
	resp ='No response'	
	if stdout:
		resp = stdout.read()
	ssh.close()
	return resp

def copyToRemote(ip,un,pwd,sourceFile,remotePath):
	ssh = getSSHClient(ip,un,pwd)
	ftp = ssh.open_sftp()
	ftp.put( sourceFile,remotePath)
	ftp.close()
	
def readRemoteFile(ip,un,pwd,remotefileName,port=22):
	'''transport = paramiko.Transport((ip, port))
   	transport.connect(username = un, password = pwd) 
	sftp = paramiko.SFTPClient.from_transport(transport)
	with open(fileName, 'r') as f:
        	data = f.read()
	return data''' 
	data =''
	unique_filename = str(uuid.uuid4())+'dhcpd.conf'
	copyRemoteFile(ip,un,pwd,remotefileName,unique_filename)

	with open(unique_filename ,'r') as f:
		data = f.read()

	os.remove(unique_filename )
	return data	 


