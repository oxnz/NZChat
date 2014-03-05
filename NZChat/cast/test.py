#!/usr/bin/env python
#-*- coding: utf-8 -*-
# server has a table of thread, which thread update the process bar

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtNetwork import *
import sys
import time

class NZFileSendThread(QThread):
	def __init__(self, parent=None):
		super(NZFileSenderThread, self).__init__(parent)
	def run(self):
		print 'run send thread'

class NZFileRecvThread(QThread):
	def __init__(self, socketDescriptor, parent=None):
		super(NZFileRecvThread, self).__init__(parent)
		self.sd = socketDescriptor
		self.done = False
	def run(self):
		self.s = QTcpSocket()
		self.connect(self.s,
				SIGNAL('error(QAbstractSocket.SocketError)'),
			SLOT(self.displayError(QAbstractSocket.SocketError)))
		if not self.s.setSocketDescriptor(self.sd):
			print 'error in set descriptor'
		self.s.readyRead.connect(self.readFileBlock)
		while not self.done:
			self.s.waitForReadyRead()
			self.s.write(QByteArray('hello from server'))
		self.s.disconnectFromHost()
		self.s.waitForDisconnected()
	def readFileBlock(self):
		pass
	def displayError(self, socketError):
		print 'error while thread processing file'

class NZFileRecvServer(QTcpServer):
	def __init__(self, parent=None):
		super(NZFileRecvServer, self).__init__(parent)
	def incomingConnection(self, socketDescriptor):
		rt = NZFileRecvThread(socketDescriptor, self)
		rt.finished.connect(rt.deleteLater)
		rt.start()

class NZFileRecvModel(QAbstractTableModel):
	def __init__(self, parent=None):
		super(NZFileRecvModel, self).__init__(parent)
		self.__sections = ['文件', '大小', '速度', '来自','进度']
		self.__tasks = []
		self.__recvServer = NZFileRecvServer(self)
#		if not self.__recvServer.listen(QHostAddress.Any, 8889):
		if not self.__recvServer.listen(QHostAddress('192.168.0.101'), 8889):
			print 'NZFileRecvServer error:', self.__recvServer.errorString()
			QMessageBox.critical(self,
					self.tr('threaded file recv'),
					self.tr('unalbe to start server: %1').
					arg(self.__recvServer.errorString()));

	def reportError(self, socketError):
		print 'a errror han'
		if socketError == QAbstractSocket.RemoteHostClosedError:
			print 'remove closed'
		elif socketError == QAbstractSocket.HostNotFoundError:
			print 'not found'
		elif socketError == QAbstractSocket.ConnectionRefusedError:
			print 'refused'
		else:
			print 'server unkonw error:', self.cc.errorString()
	def sort(self, column, order):
		print 'sort'
	def columnCount(self, index):
		return len(self.__sections)
	def rowCount(self, index):
		return len(self.__tasks)
	def headerData(self, section, orientation, role):
		results = {Qt.Vertical: {
				Qt.DisplayRole: QVariant(),
			},
			Qt.Horizontal: {
				Qt.DisplayRole: lambda: self.__sections[section],
			},
		}
		try:
			return results[orientation][role]()
		except:
			return QAbstractTableModel.headerData(self, section, orientation, role)
	def data(self, index, role):
		if not index.isValid():
			return QVariant()
		row = index.row()
		col = index.column()
		return 'test'
	def setData(self, index, value, role):
		print 'set'

class NZFileSendModel(QAbstractTableModel):
	def __init__(self, parent=None):
		super(NZFileSendModel, self).__init__(parent)
		self.__sections = ['文件', '大小', '速度', '发往','进度']
		self.__tasks = []
	def sort(self, column, order):
		print 'sort'
	def columnCount(self, index):
		return len(self.__sections)
	def rowCount(self, index):
		return len(self.__tasks)
	def headerData(self, section, orientation, role):
		results = {Qt.Vertical: {
				Qt.DisplayRole: QVariant(),
			},
			Qt.Horizontal: {
				Qt.DisplayRole: lambda: self.__sections[section],
			},
		}
		try:
			return results[orientation][role]()
		except:
			return QAbstractTableModel.headerData(self, section, orientation, role)
	def flags(self, index):
		flags = QAbstractTableModel.flags(self, index)
		flags |= Qt.ItemIsEditalbe
		return flags
	def data(self, index, role):
		if not index.isValid():
			return QVariant()
		row = index.row()
		col = index.column()
		return 'test'
	def setData(self, index, value, role):
		print 'set'

class NZFileTransfer(QFrame):
	def __init__(self,  parent=None):
		super(NZFileTransfer,  self).__init__(parent)
		self.resize(400,  300)
		vbox = QVBoxLayout(self)
		self.setLayout(vbox)
		self.sendTable = QTableView(self)
		self.sendTable.setModel(NZFileSendModel(self))
		self.sendTable.setSortingEnabled(True)
		self.sendTable.setEditTriggers(QAbstractItemView.DoubleClicked | QAbstractItemView.SelectedClicked)
		self.sendTable.horizontalHeader().setResizeMode(QHeaderView.Stretch)
		self.recvTable = QTableView(self)
		self.recvTable.setModel(NZFileRecvModel(self))
		self.recvTable.setSortingEnabled(True)
		self.recvTable.setEditTriggers(QAbstractItemView.DoubleClicked | QAbstractItemView.SelectedClicked)
		self.recvTable.horizontalHeader().setResizeMode(QHeaderView.Stretch)
		vbox.addWidget(self.sendTable)
		vbox.addStretch()
		vbox.addWidget(self.recvTable)

		sendButton = QPushButton("Send")
		recvButton = QPushButton("Recv")
		hbox = QHBoxLayout()
		hbox.addWidget(sendButton)
		hbox.addStretch()
		hbox.addWidget(recvButton)
		vbox.addLayout(hbox)

		sendButton.clicked.connect(self.sendFile)
	def sendFile(self):
		print 'send file'
	


app = QApplication(sys.argv)
x = NZFileTransfer()
x.show()
app.exec_()
