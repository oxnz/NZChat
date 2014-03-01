#-*- coding: utf-8 -*-

from NZQt import *
from NZChatWindow import NZChatWindow
from NZChatWindow import NZChatTab
from NZConfig import NZConfig
from NZContact import NZContact
from NZMessage import NZMsgType
from NZMessage import NZMessage
from NZStatus import NZStatus

class NZContactGroup(QtGui.QGroupBox):
	def __init__(self, config, addChatTab, name, parent=None):
		super(NZContactGroup, self).__init__(parent)

		self.__name = name
		self.members = dict()

		self.vbox = QtGui.QVBoxLayout(self)
		self.setLayout(self.vbox)
	@property
	def name(self):
		return self.__name
	def addContact(self, ip, contact):
		self.vbox.addWidget(contact)
		self.members[ip] = contact
	def contains(self, addr):
		return addr in self.members
	def setStatus(self, IP, status):
		print 'set status %s to %s' % (IP, status)
		self.members[IP].offline()

class NZContactPane(QtGui.QToolBox):
	def __init__(self, config, report, parent=None):
		super(NZContactPane, self).__init__(parent)

		self.config = config

#		config.monitorSocket = QtNetwork.QUdpSocket(self)
#		config.monitorSocket.bind(config.monitorPort)
		config.monitorSocket.readyRead.connect(self.readPendingDatagrams)
		self.chatWindow = NZChatWindow(config, self)

		self.groups = list([
			NZContactGroup(config, self.chatWindow.addChatTab,
				QtCore.QString(self.tr('好友')), self),
			NZContactGroup(config, self.chatWindow.addChatTab,
				QtCore.QString(self.tr('室友')), self),
			NZContactGroup(config, self.chatWindow.addChatTab,
				QtCore.QString(self.tr('黑名单')), self),
		])
		for i in self.groups:
			self.addItem(i, i.name)
		self.__defaultGroup = self.groups[0]

	def readPendingDatagrams(self):
		print 'reading broadcast datagrams ...'
		while self.config.monitorSocket.hasPendingDatagrams():
			datagram, sender, port = self.config.monitorSocket.readDatagram(self.config.monitorSocket.pendingDatagramSize())
			self.processPendingDatagram(sender.toString(), datagram)
	def processPendingDatagram(self, sender, datagram):
		msg = NZMessage.decode(datagram)
		opts = dict({
			NZMsgType.ONLINE:	self.processOnlineNotify,
			NZMsgType.OFFLINE:	self.processOfflineNotify,
			NZMsgType.KEEPALIVE:	self.processKeepAlive,
		})
		if not msg:
			return
		if msg.mtype in opts:
			opts[msg.mtype](sender, msg)
		else:
			'''here we encouter unknown type of msgs'''
			raise TypeError('Message type error with typecode of %d' % msg.mtype)
	def processOnlineNotify(self, sender, msg):
		'''if this notify is send by self, then ignore it
		'''
#		print 'got an online notify from %s' % sender, 'with contents:', msg.encode()
		self.sendOnlineNotify(QtNetwork.QHostAddress(sender))
		xin = False
		for i in self.groups:
			if i.contains(sender):
				xin = True
				#TODO set to online
				return
		if not xin:
			self.__defaultGroup.addContact(sender, NZContact(
				self.config, self.chatWindow.addChatTab,
				sender, msg.hostname, self.__defaultGroup))

	def processOfflineNotify(self, sender, msg):
		print 'got an online notify from %s' % sender
		for i in self.groups:
			if i.contains(sender):
				i.setStatus(sender, NZStatus.OFFLINE)
	def processKeepAlive(self, sender, msg):
		print 'got an keep-alive notify from %s' % sender
	def sendOnlineNotify(self, targetAddr = QtNetwork.QHostAddress.Broadcast):
#		print 'send online msg to:', sender
		if targetAddr == NZConfig.hostAddr:
			'''cause we could recv ourself online notify, and if we just
			reply to it, that would cause a infinite loop of sending online
			notify, so here just return
			'''
			return
		msg = NZMessage(mtype=NZMsgType.ONLINE).encode()
		self.config.monitorSocket.writeDatagram(msg, targetAddr, self.config.monitorPort)
	def sendOfflineNotify(self, targetAddr = QtNetwork.QHostAddress.Broadcast):
		print 'send offline notify ....'
		msg = NZMessage(mtype=NZMsgType.OFFLINE).encode()
		self.config.monitorSocket.writeDatagram(msg, targetAddr, self.config.monitorPort)
