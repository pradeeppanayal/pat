
'''
Author  : Pradeep CH
Version : Development
Since   : PAT V2
Date    : 10-Mar-2017
'''

import sys

sys.path.append('../Lib')

from sshclient import SSHClient

def triggerRemoteConsole(clientIp,serverip,un,pwd,moid):
	try:
		cmd = 'vmrc -H %s -U %s -P %s -M %s' %(serverip,un,pwd,moid)
		cl = SSHClient(clientIp)
		cl.executeCommand(cmd)
		return 'Remote console successfull'
	except Exception as e:
		assert False, 'Could not connect to remote machine. Make sure the plugin is running in your machine, Cause : %s' %str(e)
