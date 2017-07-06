#!/usr/bin/python     
__author__ ='Pradeep'


from os.path import expanduser 
import sys
import sqlite3
import os
import datetime

sourcedirectory =  expanduser("~") + "/pat/db/"
db_file =  sourcedirectory+'source.db'
logfile =  sourcedirectory+'log'
logformmat =  '%s   %s   %s\n'
ERROR ='ERROR'

class SQLDB(object):
   def __init__(self):
      self.log('Initilizing sql db')
      self.check()
      self.loadNamedEntries()

   def log(self,msg,mode='DEBUG'):
      with open(logfile,'a') as f:
           f.write(logformmat %(str(datetime.datetime.now()),mode,msg))

   def getNamedTrigger(self,name):
      entry= self.namedGetCalls[name]
      q =entry[0]
      keyset =entry[1]
      assert q, 'There is no named GET call associated to' + str(name)
      try:
         conn = sqlite3.connect(db_file) 
         cur = conn.cursor() 
         self.log(q)
         data = cur.execute(q).fetchall() 
         data = self.formatResp(data,keyset)
         return data
      except Exception as e :
         self.log(str(e),ERROR)
         if conn != None:
            conn.close()
         assert False, e 
      finally:
         conn.close()
      return 

   def addEntry(self,mapper,tablename):
      try: 
         conn = sqlite3.connect(db_file) 
         cur = conn.cursor()
         s= self.prepareAddCommand(mapper,tablename)
         self.log(s)
         cur.executescript(s)
         conn.commit() 
      except Exception as e :
         self.log(str(e),ERROR) 
         assert False, e
      finally:
         conn.close()

   def performAction(self,target,action,condition):
      self.log('Perform action called with action :'+ str(action)+', target :'+str(target)+', condition :'+ str(condition))
      q = ''
      assert target and action and condition, "invalid param"
      if action == 'delete':
         q = 'delete from '+ target +' where ' + condition
      else:
         assert False, 'Invalid action'
      self.log(q)
      try:
         conn = sqlite3.connect(db_file) 
         cur = conn.cursor()
         data = cur.executescript(q)
         conn.commit()
      except Exception as e:
         self.log(str(e),ERROR)
         if conn != None:
            conn.close()
         assert False, e
      finally:
         if conn != None:
            conn.close()

   def getData(self,tablename,keyset,key=None,keyidentifier = ''):
      try:
         conn = sqlite3.connect(db_file) 
         cur = conn.cursor()
         s= self.prepareGetQuery(tablename,keyset,key,keyidentifier) 
         self.log(s)
         data = cur.execute(s).fetchall() 
         data = self.formatResp(data,keyset)
         return data
      except Exception as e :
         self.log(str(e),ERROR)
         if conn != None:
            conn.close()
         assert False, e 
      finally:
         conn.close()

   def getDataWithCondition(self,tablename,keyset,condition):
      try:
         conn = sqlite3.connect(db_file) 
         cur = conn.cursor()
         s= self.prepareGetQuery(tablename,keyset,None,'')
         s = s + ' where ' + condition 
         self.log(s)
         data = cur.execute(s).fetchall() 
         data = self.formatResp(data,keyset)
         return data
      except Exception as e :
         self.log(str(e),ERROR)
         if conn != None:
            conn.close()
         assert False, e
      finally:
         if conn != None:
            conn.close()

   def formatResp(self,data,keyset):
       resp =[]
       for row in data:  
          r = {}
          for i in range(len(keyset)):
             r[keyset[i]] = row[i]
          resp.append(r)
       return resp

   def prepareGetQuery(self,t,ks,k,ki):
       query = 'select %s from %s ' 
       wq = '' 
       if k and type(k)==str:
          wq= ' where %s like "%s" ' %(ki,k)
       elif k and type(k)==int:
          wq= ' where %s=%d ' %(ki,k)

       query =  query %(','.join(ks),t)+wq  
       return query

   def updateEntry(self,mapper,tablename,key,keyidentifier):
      try:
         conn = sqlite3.connect(db_file) 
         cur = conn.cursor()
         s= self.prepareUpdateCommand(mapper,tablename,key,keyidentifier)
         self.log(s)
         cur.executescript(s)
         conn.commit()
      except Exception as e :
         self.log(str(e),ERROR)
         if conn != None:
            conn.close()
         assert False, e
      finally:
         if conn != None:
            conn.close()

   def prepareUpdateCommand(self,m,t,kv,ki):
      query = 'update %s set %s where %s like "%s";'
      val = [] 
      for k in m: 
          val.append('%s="%s"' %(k,m[k]))
      q=  query %(t,','.join(val),ki,kv) 
      return q

   def prepareAddCommand(self,m,t):
      query = 'insert into %s(%s) values(%s);'
      col = []
      val = []
      for k in m:
          col.append(k)
          val.append("'%s'" %m[k])
      query = query %(t,','.join(col),','.join(val))  
      return query

   def check(self): 
          self.log('Checking and creating tables')
          #create db
          try:
             conn = sqlite3.connect(db_file) 
             cur = conn.cursor()
             with open(sourcedirectory+'initialscript','r') as f:
                 s = f.read() 
             cur.executescript(s)
             conn.commit()
          except Exception as e:
             self.log(str(e),ERROR)
             if conn != None:
                conn.close()
          finally:
             try:
                 conn.close()
             except: 
                 pass
          self.log('Checking compeleted')

   def  loadNamedEntries(self):
      self.namedGetCalls = {}
      with open(sourcedirectory+'namedgetcalls','r') as f:
         s = f.readlines() 
      for line in s:
         data = line.split('::')
         key = data[0]
         q = data[1]
         keyset = data[2].split(',')
         self.namedGetCalls[data[0]]=[q,keyset]
