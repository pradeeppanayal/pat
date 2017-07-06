#!/usr/bin/python2


#Author    : Pradeep CH
#Date      : 10-Feb-2017
#Version   : 1.0.0
#Since     : 2.0.0


import uuid
import hashlib

def getRandomId():
   return str(uuid.uuid4())

def getMD5(file_name):   
   # Open,close, read file and calculate MD5 on its contents 
   with open(file_name,'rb') as file_to_check:
      # read contents of the file
      data = file_to_check.read()    
      # pipe contents of the file through
      return hashlib.md5(data).hexdigest()
