#!/usr/bin/python2



users = {'pradeep':'myword','sangeeth':'sangu','shibi':'cheera'}
def authenticate(un,pwd):
   return un in users.keys() and users[un] == pwd

