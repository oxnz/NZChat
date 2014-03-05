#-*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import  *

from NZContentPane import NZContentPane
from NZConfig import NZConfig
from NZMessage import NZMessage
from NZMessage import NZMsgType
from NZStatus import NZStatus
from NZSettings import NZSettings
from NZSockets import NZSockets

class NZAvatar(QLabel):
	'''display default avatar for newbie'''
	def __init__(self, parent=None):
		super(NZAvatar, self).__init__(parent)
		avatar = QPixmap('./avatar.png')
		avatar = avatar.scaled(64, 64)
		self.setPixmap(avatar)

class NZStatusBox(QComboBox):
	def __init__(self, config, status = NZStatus.ONLINE, parent=None):
		super(NZStatusBox, self).__init__(parent)
		self.config = config
		self.currentIndexChanged['QString'].connect(self.changeStatus)
		self.stats = dict({
			NZStatus.ONLINE : self.tr('在线'), 
			NZStatus.OFFLINE : self.tr('离线'), 
#			NZStatus.OFFLINE : self.tr('隐身'), 
		})
		for s in self.stats:
			self.addItem(self.stats[s])
	def changeStatus(self, status):
		'''handle user status change event, if needed, broadcast
		to fellows
		'''
		if status == self.stats[NZStatus.ONLINE]:
			print 'send online notify'
			msg = NZMessage(mtype=NZMsgType.ONLINE).encode()
			self.config.monitorSocket.writeDatagram(msg, QtNetwork.QHostAddress.Broadcast, self.config.monitorPort)
			del msg
		elif status == self.stats[NZStatus.OFFLINE]:
			print 'one person go offline'
			msg = NZMessage(mtype=NZMsgType.OFFLINE).encode()
			self.config.monitorSocket.writeDatagram(msg, QtNetwork.QHostAddress.Broadcast, self.config.monitorPort)
			del msg
		else:
			print 'unknow option'
	

class NZHeaderPane(QFrame):
	'''header frame of the main pane
	contains user's avatar and status combo box and nickname
	'''
	def __init__(self, config, settings, nickname, parent=None):
		super(NZHeaderPane, self).__init__(parent)
		grid = QGridLayout(self)
		self.setLayout(grid)
		grid.addWidget(NZAvatar(self), 0, 0, 2, 2)
		grid.addWidget(NZStatusBox(config, self), 0, 2, 1, 1)
		grid.addWidget(settings.account.nickname, 1, 2, 1, 1)

class NZFooterPane(QWidget):
	def __init__(self, parent=None):
		super(NZFooterPane, self).__init__(parent)
#		TODO

class NZChat(QWidget):
	def __init__(self, parent=None):
		super(NZChat, self).__init__(parent)

		# init inner resource first
		# such as socket and settings
		self.settings = NZSettings(self)
		self.sockets = NZSockets(settings)

		self.setWindowTitle(self.tr('NZChat'))
		self.resize(270, 600)
		# move to right top corner
		self.move(QApplication.desktop().width() - 400, 0)

		self.frame = QFrame(self)
		vbox = QVBoxLayout(self.frame)
		vbox.setAlignment(Qt.AlignCenter)
		self.frame.setLayout(vbox)
		self.setCentralWidget(self.frame)
		vbox.addWidget(NZHeaderPane(self.config, self), stretch = 3)
		self.contentPane = NZContentPane(self.config, self.report, self)
		vbox.addWidget(self.contentPane, stretch = 16)
		vbox.addWidget(NZFooterPane(self), stretch = 1)
	def report(self, err, level):
		print 'reporting error'
		#TODO
	def config(self):
		print 'config'
		#TODO
	def closeEvent(self, event):
		pass
		self.sendOfflineNotify()
		print 'close event handler say....'
	def sendOfflineNotify(self):
		msg = NZMessage(mtype=NZMsgType.OFFLINE).encode()
		self.config.monitorSocket.writeDatagram(msg, QtNetwork.QHostAddress.Broadcast, self.config.monitorPort)
