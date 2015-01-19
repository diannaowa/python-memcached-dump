#!/usr/bin/env python
#coding=utf-8

import socket,re
import sys

class dump(object):

	def __init__(self,host,port):
		socket.setdefaulttimeout(10)
		self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		self.s.connect((host,port))

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
	try:
		with dump('127.0.0.1',11211) as s:
			for item in s:
				print item['key'],':',item['value'] 
	except:
		print >>sys.stderr,'can\'t dump data from %s:%s' %('127.0.0.1',11211)
