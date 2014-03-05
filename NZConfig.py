#-*- coding: utf-8 -*-

from NZQt import *
import socket


class NZConfig(QtCore.QObject):
	hostname = socket.gethostname()
	hostIP =  socket.gethostbyname(hostname)
	hostAddr = None
	for a in QtNetwork.QNetworkInterface.allAddresses():
		if a.protocol() == QtNetwork.QAbstractSocket.IPv4Protocol and \
		a != QtNetwork.QHostAddress.LocalHost:
			hostAddr = a
			hostIP = a.toString()
	def __init__(self, parent=None):
		super(NZConfig, self).__init__(parent)

		self.__version = '1.01'

		self.__monitorPort = 8887
		self.__chatPort = 8888
		self.__filePort = 8889
		self.__monitorSocket = None
		self.__chatSocket = None
		self.__fileSocket = None

		self.__monitorSocket = QtNetwork.QUdpSocket(self)
		self.__monitorSocket.bind(self.__monitorPort, QtNetwork.QUdpSocket.ShareAddress)
		self.__chatSocket = QtNetwork.QUdpSocket(self)
		self.__chatSocket.bind(QtNetwork.QHostAddress(NZConfig.hostIP),
				self.__chatPort)

		self.__fileSocket = QtNetwork.QTcpSocket(self)

	@property
	def version(self):
		return self.__version
	@property
	def monitorPort(self):
		return self.__monitorPort
	@monitorPort.setter
	def monitorPort(self, port):
		self.__monitorPort = port
	@property
	def chatPort(self):
		return self.__chatPort
	@chatPort.setter
	def chatPort(self, port):
		self.__chatPort = port
	@property
	def filePort(self):
		return self.__filePort
	@filePort.setter
	def filePort(self, port):
		self.__filePort = port
	@property
	def monitorSocket(self):
		return self.__monitorSocket
	@monitorSocket.setter
	def monitorSocket(self, socket):
		if not self.__monitorSocket == None:
			self.__monitorSocket.close()
		self.__monitorSocket = socket
	@property
	def chatSocket(self):
		return self.__chatSocket
#	@chatSocket.setter
#	def chatSocket(self, socket):
#		if not self.__chatSocket == None:
#			self.__chatSocket.close()
#		self.__chatSocket = socket
