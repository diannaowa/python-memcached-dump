#!/usr/bin/env python
#coding=utf-8

import socket,re
import sys,argparse
import json

class dump(object):

	def __init__(self,**kwargs):
		socket.setdefaulttimeout(10)
		self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		self.s.connect((kwargs.get('host'),kwargs.get('port')))
		
	#return [{'key':'key','len':4,'value':'1234'}]
	def __enter__(self):
		result = []
		itemsPack = self.__sendCmd('stats items\n') 
		items = self.__unpackItems(itemsPack)
		keys = self.__unpackKeys(items)
		for d in self.__getData(keys):
			result.append({"key":d[0],"len":d[1],"value":d[2]})
		return result	
	def __exit__(self,*args):
		return self.s.close()

	def __sendCmd(self,cmd):
		result = list()
		self.s.send(cmd)
		while True:
			data = self.s.recv(2048)
			if not data:
				break
			result.append(data)
			if 'END' in data:
				break
		return ''.join(result)
	
	def __unpackItems(self,data):
		items = re.findall('STAT items:(\d+):number (\d+)',data)
		return items

	def __unpackKeys(self,data):
		keys = list()
		for item in data:
			cmd = "stats cachedump "+item[0]+" "+item[1]+'\n'
			keyStr = self.__sendCmd(cmd)
			key = re.findall('ITEM ([^\s]+) \[(\d+) b',keyStr)
			for k in key:
				if int(k[1]) != 0:
	 				keys.append((k[0],k[1]))
		return keys

	def __getData(self,data):
		for key in data:
			d = re.search('\\r\\n(?P<value>[^\s]+)',self.__sendCmd('get '+key[0]+'\n')).groupdict()
			yield key[0],key[1],d['value']
			
	
if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('--host',action='store',dest='host',default='127.0.0.1',help='memcached server host,default[127.0.0.1]')
	parser.add_argument('--port',action='store',dest='port',default='11211',help='memcached server port,default[11211]')
	parser.add_argument('--path',action='store',dest='path',default='/tmp/memcached.json',help='File path,default[/tmp/memcached.json]')
	args = parser.parse_args()
	hostPort = {'host':args.host,'port':int(args.port)}
	try:
		with dump(**hostPort) as dumpInst:
			data = dumpInst
	except:
		print >>sys.stderr,'can\'t dump data from %s:%s' %(args.host,args.port)
	try:	
		with open(args.path,'w') as fp:
			json.dump(data,fp)
	except:
		print >>sys.stderr,'can\'t open or write file %s' % args.path
