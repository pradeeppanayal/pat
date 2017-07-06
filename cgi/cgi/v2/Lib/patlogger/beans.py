
import datetime
import os
from os.path import expanduser 


sourcedirectory =  expanduser("~") + "/pat/"
directory = sourcedirectory +'logs/'
logFormat ='\r\n%s %s %s' 


class PATLogger(object):
   def __init__(self,sourceName):
      self.clzz = sourceName
      self.fname = directory+sourceName+'.log'
   def log(self,msg,mode='debug'):
      t= str(datetime.datetime.now())
      log = logFormat %(t,self.clzz,msg)
      wm = 'w'
      if os.path.exists(self.fname):
          wm = 'a'
      with open(self.fname,wm) as f:
         f.write(log)


 
