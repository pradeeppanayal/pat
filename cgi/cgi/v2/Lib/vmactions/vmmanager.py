#!/usr/bin/python

#################################

# Author  : Pradeep CH
# Version : 1.0.0
# Since   : PAT 2.0.0
# Date    : Apr-06-2017

#################################

import sys

sys.path.append('../')

from ParamikkoUtil import executeCommand

startCommandFormat = 'vim-cmd vmsvc/power.on %s'
stopCommandFormat  = 'vim-cmd vmsvc/power.off %s' 

def start(ip,un,pwd,moid): 
   #executeCommand(ip,username,password,cmd):
   executeCommand(ip,un,pwd,startCommandFormat %moid) 

def stop(ip,un,pwd,moid):
   executeCommand(ip,un,pwd,stopCommandFormat %moid) 

