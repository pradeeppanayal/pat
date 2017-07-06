__author__='Pradeep CH'
__version__ ='1.0.0'
__date__= '10- Mar- 2017'

import json
from beans import Config,Pool,Host,Subnet

class JsonParser(object): 
    @staticmethod
    def parse(jsonData):
      c = Config()
      jsonObj = json.loads(jsonData)
      subnets = jsonObj['subnets']
      for subnet in subnets:
         s= Subnet()
         pools = subnet['pools']
         for pool in pools:
            p = Pool()
            hosts = pool['hosts']
            for host in hosts:
               h = Host()
               h.mac = host['mac']
               h.ip = host['ip']
               p.hosts.append(h)
            p.rangeStart = pool['rangeStart']
            p.rangeEnd = pool['rangeEnd']
            p.bootfileName = pool['bootfileName']
            p.subnetMask = pool['subnetMask']
            p.status = pool['status']
            p.routers = pool['routers'] 
            p.assignedDate = pool['assignedDate']
            s.pools.append(p)
         hosts = subnet['hosts']
         for host in hosts:
            h = Host()
            h.mac = host['mac']
            h.ip = host['ip']
            s.hosts.append(h)
 
         s.subnet= subnet['subnet']
         s.netmask= subnet['netmask']
         c.subnets.append(s)
      return c


