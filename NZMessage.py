#-*- coding: utf-8 -*-

from NZQt import *
import json
import time
from NZConfig import NZConfig

class NZMsgType():
	'''FOLLOWUP stands for that the msg recieved previous is not complete,
	this msg is a follow-up
	'''
	ONLINE		= 0x01
	OFFLINE		= 0x02
	KEEPALIVE	= 0x03
	TEXTMSG		= 0x04
	FOLLOWUP	= 0x05

class NZMessage(QtCore.QObject):
	def __init__(self, mtype, time = time.strftime("%F %T"), hostname=NZConfig.hostname, version = NZConfig.version, data=None):
		super(NZMessage, self).__init__()
		self.__version = str(version)
		self.__hostname = str(hostname)
		self.__type = mtype
		self.__time = str(time)
		self.__data = str(data)
	@property
	def mtype(self):
		return self.__type
	@property
	def hostname(self):
		return self.__hostname
	@hostname.setter
	def hostname(self, hostname):
		self.__hostname = hostname
	@property
	def time(self):
		return self.__time
	@property
	def data(self):
		return self.__data
	@data.setter
	def data(self, data):
		self.__data = data
	@classmethod
	def decode(cls, dict_):
		if isinstance(dict_, type(NZMessage)):
			return dict_
		try:
			d = json.loads(dict_, encoding='utf-8')
			return NZMessage(d['type'], d['time'], d['hostname'], d['version'], d['data'])
		except ValueError as e:
			raise ValueError('Message decode error with error info (%s)' % e)
		except:
			raise RuntimeError('Message decode error with unkonw cause')
		return None
	def encode(self):
		return QtCore.QByteArray(json.dumps({
			'version':	self.__version,
			'hostname':	self.__hostname,
			'type':		self.__type,
			'time':		self.__time,
			'data':		self.__data,
		}, encoding='utf-8'))

if __name__ == '__main__':
	m = NZMessage(NZMsgType.TEXTMSG, data='你好, this is a test massage')
	print '---------encode-----------\n', m.encode(), type(m.encode())
	print '---------dcode------------'
	print NZMessage.decode(m.encode()).encode()
