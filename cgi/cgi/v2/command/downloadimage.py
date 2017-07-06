#!/usr/bin/python
 
import sys
# Import modules for CGI handling 
import cgi, cgitb 
import os

tempLoc = '/tmp/eosimages'
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

def main():
   form = cgi.FieldStorage()
   fname =  form.getvalue('fname') 
   filePath = tempLoc+'/' + fname
   assert os.path.exists(filePath),'No image file'
   initiateFileDownload(filePath,fname)

if __name__ == "__main__":
   try:
      main()
   except Exception as e :
      print "Content-type:text/html\r\n\r\n"
      print {'status':'error','data':'Something went wrong. Cause :' + str(e)}
