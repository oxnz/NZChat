#-*- coding: utf-8 -*-
from NZQt import *
from NZContentPane import NZContentPane
from NZConfig import NZConfig
from NZMessage import NZMessage
from NZMessage import NZMsgType
from NZStatus import NZStatus

QtCore.QTextCodec.setCodecForLocale(QtCore.QTextCodec.codecForName('utf8'))
QtCore.QTextCodec.setCodecForLocale(QtCore.QTextCodec.codecForName('utf8'))
QtCore.QTextCodec.setCodecForTr(QtCore.QTextCodec.codecForName('utf8'))

class NZAvatar(QtGui.QLabel):
	'''display default avatar for newbie'''
	def __init__(self, parent=None):
		super(NZAvatar, self).__init__(parent)
		avatar = QtGui.QPixmap('./avatar.png')
		avatar = avatar.scaled(64, 64)
		self.setPixmap(avatar)

class NZStatusBox(QtGui.QComboBox):
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
	

class NZHeaderPane(QtGui.QFrame):
	'''header part of the main pane
	contains user's avatar and status combo box and nickname
	'''
	def __init__(self, config, parent=None):
		super(NZHeaderPane, self).__init__(parent)
		grid = QtGui.QGridLayout(self)
		self.setLayout(grid)
		grid.addWidget(NZAvatar(self), 0, 0, 2, 2)
		grid.addWidget(NZStatusBox(config, self), 0, 2, 1, 1)
		grid.addWidget(QtGui.QLabel(self.tr('John Snow')), 1, 2, 1, 1)


class NZFooterPane(QtGui.QWidget):
	def __init__(self, parent=None):
		super(NZFooterPane, self).__init__(parent)
#		TODO

#class NZChat(QtGui.QWidget):
class NZChat(QtGui.QMainWindow):
	def __init__(self, parent=None):
		super(NZChat, self).__init__(parent)

		self.config = NZConfig(self)

		self.setWindowTitle(self.tr('NZChat'))
		self.resize(270, 600)
		# move to right top corner
		self.move(QtGui.QApplication.desktop().width() - 400, 0)

		self.frame = QtGui.QFrame(self)
		vbox = QtGui.QVBoxLayout(self.frame)
#		vbox = QtGui.QVBoxLayout(self)
		vbox.setAlignment(QtCore.Qt.AlignCenter)
#		self.setLayout(vbox)
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
