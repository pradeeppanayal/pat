__author__='Pradeep CH'
__version__ ='1.0.0'
__date__= '10- Mar- 2017'

import sys
sys.path.append('/home/local/PAYODA/pradeep.k/Python/DHCP Hosts/')
import re
from dhcpconfig import Config,Pool,Host,Subnet

class DHCPDConfigParser(object):

   @staticmethod
   def parse(data):
      conf = Config()
      data =DHCPDConfigParser.preprocess(data) 
      blocks = DHCPDConfigParser.getAsBlocks(data)
      subnetBlocks = blocks['subnet']     
       
      for subnetBlock in subnetBlocks: 
          subnet = DHCPDConfigParser.extractSubnet(subnetBlock)
          subnetSpecBlocks = DHCPDConfigParser.getAsBlocks(subnetBlock)
          poolBlocks = subnetSpecBlocks['pool']
          sHostBlocks = subnetSpecBlocks['host']  
          for poolBlock in poolBlocks:
             pool = DHCPDConfigParser.extractPool(poolBlock)
             poolSpecBlocks =  DHCPDConfigParser.getAsBlocks(poolBlock)
             pHostBlocks = poolSpecBlocks['host'] 
             for hostBlock in pHostBlocks:
                host =  DHCPDConfigParser.extractHost(hostBlock)
                pool.hosts.append(host)
             subnet.pools.append(pool)
 
          for hostBlock in sHostBlocks:
             host =  DHCPDConfigParser.extractHost(hostBlock)
             subnet.hosts.append(host)

          conf.subnets.append(subnet)
      return conf

   @staticmethod
   def extractHost(hostBlock): 
      host = Host()
      host.name = re.search('host +([-\w.]*)?[\s{]*',hostBlock).group(1)
      host.mac =  re.search('hardware +ethernet +(\S*)? *;',hostBlock).group(1)
      host.ip =  re.search('fixed-address +(\S*)? *;',hostBlock).group(1)      
      return host

   @staticmethod
   def extractPool(poolBlock): 
      pool = Pool() 
      m = re.search('range (\S+)? +(\S+)? *;',poolBlock) 
      pool.rangeStart = m.group(1)
      pool.rangeEnd = m.group(2)
      pool.bootfileName =  re.search('option +bootfile-name +"(\S*)?"',poolBlock).group(1)
      pool.subnetMask =  re.search('option +subnet-mask +(\S*)? *;',poolBlock).group(1)
      pool.routers =  re.search('option +routers +(\S*)? *;',poolBlock).group(1)
      if pool.bootfileName :
         pool.status = 'Assigned'
      return pool

   @staticmethod
   def extractSubnet(subnetBlock):
       subnet =Subnet()
       line = subnetBlock[:subnetBlock.index('\n')]
       items = re.split('\s+',line)
       subnet.subnet = items[1]
       subnet.netmask = items[3]
       return subnet


   @staticmethod
   def getAsBlocks(data):
      subnetBlocks =[]
      poolBlocks = []
      hostBlocks =[]
      ci = 1
      pi = 1
      while ci!=-1 and ci<len(data):  
          line = data[pi:ci]   
          ri = 0
          if line.startswith('subnet'):  
             [ri,subnetblock] = DHCPDConfigParser.extractBlock(data[pi:])
             subnetBlocks .append(subnetblock)
          elif line.startswith('pool'):
             [ri,poolblock] = DHCPDConfigParser.extractBlock(data[pi:])
             poolBlocks .append(poolblock)
          elif line.startswith('host'):
             [ri,hostBlock] = DHCPDConfigParser.extractBlock(data[pi:])
             hostBlocks .append(hostBlock)
          try:
             if ri==0:
                pi = ci
             else:
                pi +=ri+1
             ci = data.index('\n',pi+1)+1
          except Exception as e: 
             ci =-1
          
      return {'subnet':subnetBlocks,'pool':poolBlocks,'host':hostBlocks}
   
   @staticmethod
   def extractBlock(data): 
      si = data.index('{')
      ci = si
      if si==-1:
         return ''
      lc = 1
      rc = 0

      while lc > rc and ci < len(data):
          ci +=1
          c = data[ci]
          if  c == '{':
             lc +=1
          elif c == '}':
             rc +=1
      return [ci+1,data[:ci+1]]
   
   @staticmethod
   def preprocess(data):
      processedData =''
      cIndex= 0
      commentStarted = False
      newLine = False

      while cIndex< len(data):
         c = data[cIndex]
         cIndex +=1
         if  c=='#':
            commentStarted = True
            continue
         if c == '\n':
            commentStarted = False
            newLine = True
            continue 
         if commentStarted or (newLine and (c==' ' or c=='\t')): 
            continue

         if newLine:
            processedData +='\n'
            newLine = False
         processedData +=c 
      return processedData
      
