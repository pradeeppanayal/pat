#!/usr/bin/python2
 
import sys
import os
import subprocess
import datetime
import zipfile
import shutil

sys.path.append('../Lib')
import re
import json

from commandexecutor import executeCommandSSH 

import cgi, cgitb 

__author__ ='Pradeep CH'
__version__='1.0.0'

parentFolder ='resources'
caFile ='%s/caList' %parentFolder 
caCertLoca = 'ROOT'
csrReqLoc = 'CSR'
userCertLoc = 'USERCERTS'
signedCertLoc = 'SIGNEDCERT'
deviceCertLoc = 'DEVICECERT'

sampleConfigFileLocation = '%s/openssl.cnf' %parentFolder;
cadirIdentifier = '<CA ROOT DIR>'
privateKeyRef = '<privatekey>'
publicKeyRef = '<publickey>'

def log(msg,level='DEBUG'):
	with open('log','a') as f:
		fmsg = '\n%s\t%s\t%s' %(str(datetime.datetime.now()) ,level, str(msg))
		f.write(fmsg)

def loadCA():		 
	resp = '{}'
	if not os.path.exists(caFile):
		open(caFile,'w').write('[]')		
	try:
		with open(caFile,'r') as f:
			data = f.read()
			data = json.loads(data) 
			resp = {'status':'SUCCESS','data':data}
	except Exception as e:
		resp ={'status':'ERROR','data':str(e)}
	return json.dumps(resp);

def createFolderStructure(cn):
	directory = '%s/%s' %(parentFolder,cn)
	
	if not os.path.exists(directory):
		os.makedirs(directory)
		os.makedirs('%s/%s' %(directory,caCertLoca))
		os.makedirs('%s/%s' %(directory,csrReqLoc))
		os.makedirs('%s/%s' %(directory,userCertLoc))
		os.makedirs('%s/%s' %(directory,deviceCertLoc))
		os.makedirs('%s/%s' %(directory,signedCertLoc))
	
	with open('%s/serial' %directory,'w') as f:
		f.write('1000')
	with open('%s/index.txt' %directory,'w') as f:
		pass
	
def copyConfigFile(cn):
	caLoc = '%s/%s' %(parentFolder,cn)	
	privateKeyLoc = '%s/%s-private.key' %(caCertLoca,cn)
	publicKeyLoc = '%s/%s-public.cert' %(caCertLoca,cn)
	configFileLocation = '%s/%s/openssl.conf' %(parentFolder,cn)
	
	with open(sampleConfigFileLocation,'r') as f:
		data = f.read()
		assert data !=None and len(data)>0, 'No config file'
		data = data.replace(cadirIdentifier,caLoc)
		data = data.replace(privateKeyRef,privateKeyLoc)
		data = data.replace(publicKeyRef,publicKeyLoc) 

		with open(configFileLocation,'w') as cFile:
			cFile.write(data)

def addToCAList(cn,org,orgUnit,country,email,state,locality): 
	data =None
	with open(caFile,'r') as f:
		data = f.read()
	with open(caFile,'w') as f:
		if data ==None or data == '':
			data =[]
		else:
			data = json.loads(data) 
		data.append({'cn':cn,'org':org,'orgUnit':orgUnit,'country':country,'email':email,'state':state,'locality':locality})
		f.write(json.dumps(data) )

		
def addCA(cn,email,org,country,state,locality,orgUnit,update=False):
	directory = '%s/%s' %(parentFolder,cn)
	rootDirectory = '%s/ROOT' %directory
	isFolderExist = os.path.exists(directory)
	if isFolderExist and not update:
    		return {'status':'ERROR','data':'Common name already exist'}
	elif not isFolderExist:
		createFolderStructure(cn);
	
	bashCommand = "openssl req -subj '/CN=%s/O=%s/OU=%s/C=%s/emailAddress=%s/ST=%s/L=%s' -new -newkey rsa:2048 -days 365 -nodes -x509 -keyout %s/%s-private.key -out %s/%s-public.cert" %(cn,org,orgUnit,country,email,state,locality,rootDirectory,cn,rootDirectory,cn)
	try: 
		output = executeCommand(bashCommand)
		if output:
			copyConfigFile(cn)
			addToCAList(cn,org,orgUnit,country,email,state,locality)
			return {'status':'SUCCESS','data':'Cert successfully created. Actual resp : ' + str(output)} 
		else:
			return {'status':'ERROR','data':'Cert creation failed' + output} 			
	except Exception as e:	
		try:
			#delete the folder
			shutil.rmtree(directory)
		except:
			pass	
		return {'status':'ERROR','data':'Exception %s' %str(e)} 

def generateUserCert(ca,un):		
	try: 
		downloadFileName = '%s-user.zip' %un
		
		privateKeyName = '%s-private.pem' %un
		certName = '%s-cert.pem' %un

		[userCSRLoc,privateKeyLoc] = createUserCsr(ca,un) 
		signedCertPath = signUserCSR(userCSRLoc,ca,un) 
		files = [{'file':privateKeyLoc,'fileName':privateKeyName},{'file':signedCertPath,'fileName':certName}]
		zipFile = zipFiles(files,downloadFileName)
		initiateFileDownload(zipFile,downloadFileName,True)  
		try:
			os.remove(signedCertPath)
		except:
			pass
	except Exception as e: 
		return {'status':'ERROR','data':'Exception %s' %str(e)} 

def generateDeviceCert(ca,deviceName):		
	try: 
		downloadFileName = '%s-device.zip' %deviceName
		
		privateKeyName = '%s-private.pem' %deviceName
		certName = '%s-cert.pem' %deviceName

		[deviceCSRLoc,privateKeyLoc] = createDeviceCsr(ca,deviceName) 
		signedCertPath = signDeviceCSR(deviceCSRLoc,ca,deviceName) 
		files = [{'file':privateKeyLoc,'fileName':privateKeyName},{'file':signedCertPath,'fileName':certName}]
		zipFile = zipFiles(files,downloadFileName)
		initiateFileDownload(zipFile,downloadFileName,True)  
		try:
			os.remove(signedCertPath)
		except:
			pass
	except Exception as e: 
		return {'status':'ERROR','data':'Exception %s' %str(e)} 

def zipFiles(files,fileName):
	fullPath = '%s/%s' %(parentFolder,fileName)
	with zipfile.ZipFile(fullPath, "w") as f:
		for fileItem in files:
			f.write(fileItem['file'],fileItem['fileName'])
	return fullPath

def download(cn,act):
	rootDirectory = '%s/%s/ROOT' %(parentFolder,cn)
	fullPath = ''
	downloadFileName = ''

	if act == 'downloadPrivate':
		downloadFileName = '%s-private.key' %cn 
	else:
		downloadFileName = '%s-public.cert' %cn 

	fullPath = '%s/%s' %(rootDirectory,downloadFileName)

	try:
		initiateFileDownload(fullPath,downloadFileName,False)  
	except Exception as e:
		print "Content-type:text/html\r\n\r\n"
		print 'Unexpected error occured. %s' %str(e)

def executeCommand(cmd):
	
	output = subprocess.check_call(cmd, shell=True) 
	log('Command %s :::: Output %s' %(str(cmd),str(output)))
	return output==0 

def storeCSR(csr,csrName,caDir):
	csrFileName = '%s/%s/%s' %(caDir,csrReqLoc,csrName)
	with open(csrFileName,'wb') as f:
		f.write(csr.file.read())
	return csrFileName

def signCSR(csrFile,caLoc,targetFileName,validity="375"):
	confFileName = '%s/openssl.conf' %(caLoc)
	targetFile = '%s/%s/%s' %(caLoc,signedCertLoc,targetFileName)
	cmd  = 'openssl ca -batch -config %s -extensions server_cert -days %s -notext -md sha256 -in %s -out %s' %(confFileName,validity,csrFile,targetFile) 
	if executeCommand(cmd):
		return  targetFile

def signUserCSR(userCertLoc,ca,un):
	targetFileName = '%s_user_cert.pem' %(un)
	caLoc ='%s/%s' %(parentFolder,ca)
	confFileName = '%s/openssl.conf' %(caLoc)
	targetLocation = '%s/%s/%s' %(caLoc,signedCertLoc,targetFileName)

	cmdSign = 'openssl ca  -batch -config %s -extensions usr_cert -days 375 -notext -md sha256 -in %s -out %s' %(confFileName,userCertLoc,targetLocation)
	if executeCommand(cmdSign):
		return  targetLocation

def createUserCsr(ca,un): 
	global parentFolder,userCertLoc
	userDirctory = '%s/%s/%s' %(parentFolder,ca,userCertLoc) 

	privateKeyLoc = '%s/%s_privkey.pem' %(userDirctory,un) 
	userCSRLoc =  '%s/user-%s.csr' %(userDirctory,un)

	cmdCsr = 'openssl req -new -newkey rsa:2048 -nodes -subj "/CN=%s/O=PAYODA/OU=ARISTA/C=IN/emailAddress=user@payoda.com/ST=CBE/L=CBE" -keyout %s -out %s' %(un,privateKeyLoc,userCSRLoc)
	if executeCommand(cmdCsr):
		return  [userCSRLoc,privateKeyLoc]

def signDeviceCSR(deviceCertLoc,ca,deviceName):
	targetFileName = '%s_user_cert.pem' %(deviceName)
	caLoc ='%s/%s' %(parentFolder,ca)
	confFileName = '%s/openssl.conf' %(caLoc)
	targetLocation = '%s/%s/%s' %(caLoc,signedCertLoc,targetFileName)

	cmdSign = 'openssl ca  -batch -config %s -extensions server_cert -days 375 -notext -md sha256 -in %s -out %s' %(confFileName,deviceCertLoc,targetLocation)
	if executeCommand(cmdSign):
		return  targetLocation

def createDeviceCsr(ca,deviceName): 
	global parentFolder,userCertLoc
	deviceDirctory = '%s/%s/%s' %(parentFolder,ca,deviceCertLoc) 

	privateKeyLoc = '%s/%s_privkey.pem' %(deviceDirctory,deviceName) 
	userCSRLoc =  '%s/device-%s.csr' %(deviceDirctory,deviceName)

	cmdCsr = 'openssl req -new -newkey rsa:2048 -nodes -subj "/CN=%s/O=PAYODA/OU=ARISTA/C=IN/emailAddress=user@payoda.com/ST=CBE/L=CBE" -keyout %s -out %s' %(deviceName,privateKeyLoc,userCSRLoc)
	if executeCommand(cmdCsr):
		return  [userCSRLoc,privateKeyLoc]


def initiateFileDownload(filePath,downloadFileName,remove=False):
	if filePath:
		data = '' 
		with open(filePath,'r') as f:
			data = f.read()

		print 'Content-Disposition: attachment; filename="%s"' % downloadFileName
		#print "Content-Length: " + str(os.stat(fullPath).st_size)
		print    # empty line between headers and body
		print data
		try:
			if remove:
				os.remove(filePath)
		except:
			pass
	else:
		print "Content-type:text/html\r\n\r\n"
		print '{"status":"ERROR","data":"No files to download"}'
	
def uploadAndSignCSR(ca,CSR,csrName,validity):
	#print "Content-type:text/html\r\n\r\n"
	#print
	caDir = '%s/%s' %(parentFolder,ca)
	#print caDir
	csrFileName = storeCSR(CSR,csrName,caDir)
	#print csrFileName
	targetFileName = '%s-signed.cert' %csrName
	try:
		targetCertPath = signCSR(csrFileName,caDir,targetFileName,validity)
		initiateFileDownload(targetCertPath,targetFileName,True) 
	except Exception as e:
		print "Content-type:text/html\r\n\r\n"
		print 'Unexpected error occured. %s' %str(e)

def main():
	form = cgi.FieldStorage()  
	act = form.getvalue('action') 	  
	if(act == 'loadCA'):
		resp = loadCA() 
		print 'Content-type:text/html\r\n' 
		print resp
	elif act == 'addCA':
		cn = form.getvalue('cn') 
		
		email = form.getvalue('email') 
		country = form.getvalue('country') 
		org = form.getvalue('org') 
		state = form.getvalue('state') 
		locality = form.getvalue('locality') 
		orgUnit = form.getvalue('orgUnit') 
		assert cn and email and org and country and state and locality and orgUnit,'Invalid Params'
		assert not " " in cn,'Commnon name should not have space'
		
		resp = addCA(cn,email,org,country,state,locality,orgUnit)

		print 'Content-type:text/html\r\n'
		print json.dumps(resp) 
	elif act=='downloadPrivate' or act=='downloadCert':
		ca = form.getvalue('ca')
		download(ca,act)	
	elif act=='csr':	
		uploadedFile = form['csrFile'] 
		fileName = uploadedFile.filename
		cn =  form.getvalue('ca') 
		validity =  form.getvalue('validity') 
		assert fileName, 'Invalid file name'
		if not 	validity:
			validity = "375"
		validity = str(validity)
		assert validity.isdigit(), 'Invalid validity'
		
		uploadAndSignCSR(cn,uploadedFile,fileName,validity)
	elif act =='userCert':  
		cn =  form.getvalue('ca') 
		un =  form.getvalue('username') 
		assert un, 'Invalid username'	 
		resp = generateUserCert(cn,un)
		if resp :
			print 'Content-type:text/html\r\n'
			print json.dumps(resp)
	elif act =='deviceCert':  
		ca =  form.getvalue('ca') 
		deviceName =  form.getvalue('deviceName') 
		assert deviceName, 'Invalid device name'	 
		resp = generateDeviceCert(ca,deviceName)
		if resp :
			print 'Content-type:text/html\r\n'
			print json.dumps(resp)
	else:
		print 'Content-type:text/html\r\n'
		print '{"status":"ERROR","data":"Invalid action"}'  

if __name__ == "__main__":
   try:
      main()
   except Exception as e :
      print 'Content-type:text/html\r\n'
      print json.dumps({'status':'ERROR','data':'Exception %s' %str(e)})
  


