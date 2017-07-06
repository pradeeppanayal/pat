#!/usr/bin/python

# Import modules for CGI handling 
import cgi, cgitb 
import os
from os.path import expanduser 
import sys
import json
import datetime

sys.path.append('../Lib') 

from sqldb import db

#
#Author Pradeep CH
#
__author__ ='Pradeep CH'
__version__='1.0.0'
  
sourcedirectory =  expanduser("~") + "/pat/"
sourcePath  = sourcedirectory + 'properties'
mediaPath =''
URLMediaPath =''


#Extract the storage location
with open(sourcePath,'r') as f:
   lines = f.readlines()
   for line in lines:
      line.startswith('MEDIAPATH')
      parts = line.split(' ')
      mediaPath = parts[1]
      URLMediaPath =parts[2]


def storeFile(fileName,data):
   with open(fileName,'wb') as f:
      f.write(data)
def addEntry(fileName,subject,description,path,mediaType):   
   db.addEntry({'filename':fileName,'subject':subject,'desc':description,'path':path,'date':str(datetime.datetime.now().date()),'mediatype':mediaType},'Library');

def upload(form): 
   name =  form.getvalue('name')
   destPath = mediaPath + name
   assert not os.path.exists(destPath), 'File already exist'
   try:
      uploadedFile = form['sourcefile']
      subject =  form.getvalue('subject')
      desc =  form.getvalue('desc')
      mediaType =  form.getvalue('mediatype')
      assert subject and desc, 'Subject and description canot be empty'
      fileName = uploadedFile.filename 
      assert fileName, 'Invalid file name'
      destPath = mediaPath + name
      urlPath = URLMediaPath + name
      storeFile(destPath,uploadedFile.file.read())
      addEntry(name,subject,desc,urlPath,mediaType)
      return {'status':'success','data':'File upload successfull'}
   except Exception as e: 
      try:
         os.remove(destPath)
      except Exception as f: 
         pass
      return {'status':'error','data':'File upload failed. Reson :' + str(e)}

def search(keyword):
   searchKeySet = ['filename','subject','desc','date']
   keySet = ['filename','subject','desc','path','date','id','mediatype']
   condition = ''
   if not keyword:
      keyword = ''
   for key in searchKeySet:
      if condition != '':
         condition +=' or '

      condition += key+' like '+'"%'+keyword+'%"'
  
   data =db.getDataWithCondition('Library',keySet,condition)
   return {'status':'success','data':data}
def download(fname):
   locaPath = mediaPath + fname
   assert os.path.exists(locaPath), 'Requested file does not exist'  
   try: 
      with open(locaPath,'r') as f:
          data = f.read()
      print 'Content-Disposition: attachment; filename="%s"' % fname
      #print "Content-Length: " + str(os.stat(fullPath).st_size)
      print    # empty line between headers and body
      print data

   except Exception as e:
      print "Content-type:text/html\r\n\r\n"
      print 'Unexpected error occured. %s' %str(e)

def delete(fname):
   locaPath = mediaPath + fname
   #assert os.path.exists(locaPath), 'Requested file does not exist'  
   try:
      db.performAction('Library','delete',' filename like "'+fname+'";')
      os.remove(locaPath)
      return {'status':'success','data':'File deleted'}
   except Exception as e:
      return {'status':'error','data':'File may be already deleted or currepted'}

def main():
   form = cgi.FieldStorage()  
   action =  form.getvalue('action')
   #resp = json.loads("{}")
   if action=='upload':
      resp = upload(form)
   elif action == 'search':
      keyword =  form.getvalue('keyword')
      resp = search(keyword) 
   elif action=='download':
      fname= form.getvalue('fname')
      download(fname)
   elif action=='delete':
      fname= form.getvalue('fname')
      resp = delete(fname)
   else:
      resp = {'status':'error','data':'invalid action'}

   if action!='download':
      print 'Content-type:text/html\r\n'
      print json.dumps(resp)
if __name__=='__main__':
   
   try:
      main()
   except Exception as e:
      print 'Content-type:text/html\r\n'
      print json.dumps({'status':'error','data':'Exception ' +str(e)})
