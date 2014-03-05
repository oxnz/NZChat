#!/usr/bin/python

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtNetwork import *
import socket
import sys
import time

class NZFileRecvThread(QThread):
	def __init__(self, socketDescriptor, parent=None):
		super(NZFileRecvThread, self).__init__(parent)
		self.sd = socketDescriptor
		self.done = False
		self.x = 10
	def run(self):
		self.s = QTcpSocket()
		self.connect(self.s,
				SIGNAL('error(QAbstractSocket.SocketError)'),
				SLOT(self.errorX(QAbstractSocket.SocketError)))
		if not self.s.setSocketDescriptor(self.sd):
			print 'error in set descriptor'
		print 'state=', self.s.state(),'error=', self.s.error()
		while not self.done:
			self.s.waitForReadyRead(-1)
			self.readX()
		self.s.disconnectFromHost()
	def readX(self):
		d = self.s.readAll()
		print 'd=', d
		self.s.write(QByteArray('msg from server'))
		self.x -= 1
		self.done = self.x == 0
	def errorX(self, socketError):
		print '*** socketError:',  self.s.errorString()
class NZFileRecvServer(QTcpServer):
	def __init__(self, parent=None):
		super(NZFileRecvServer, self).__init__(parent)
	def incomingConnection(self, socketDescriptor):
		print 'incoming connection'
#		self.s = QTcpSocket()
#		self.s.setSocketDescriptor(socketDescriptor)
#		print 'connection request from:', self.s.peerAddress().toString()
#		self.s.readyRead.connect(self.readX)
		rt = NZFileRecvThread(socketDescriptor, self)
		rt.finished.connect(rt.deleteLater)
		rt.start()
	def readX(self):
		d = self.s.readAll()
		print 'thread reading:', d
		self.s.write(QByteArray('hi, there'))

class NZFileTransfer(QWidget):
	def __init__(self, parent=None):
		super(NZFileTransfer,  self).__init__(parent)
		self.setWindowTitle('server')
		self.resize(200, 100)

		vbox = QVBoxLayout(self)
		self.setLayout(vbox)
		sendButton = QPushButton('send')
		sendButton.clicked.connect(self.sendData)
		vbox.addWidget(sendButton)
		recvButton = QPushButton('recv')
		recvButton.clicked.connect(self.readData)
		vbox.addWidget(recvButton)

		self.ss = NZFileRecvServer()
#		self.ss = QTcpServer()
		self.ss.listen(QHostAddress('192.168.0.101'), 8889)
#		self.ss.newConnection.connect(self.newClient)

		self.ccs = []
	def newClient(self):
		print 'new client'
		self.cc = self.ss.nextPendingConnection()
		self.cc.write(QByteArray('msg from server'))
		self.ccs.append(self.cc)

		self.cc.readyRead.connect(self.readData)
		self.cc.disconnected.connect(self.offline)
		self.cc.error.connect(self.gotError)
	def gotError(self):
		print 'error occured'
	def offline(self):
		print 'client go offline'
	def readData(self):
		for s in self.ccs:
			print '-----server read--------'
			d = s.readAll()
			print d
			print '=======server read========'

	def sendData(self):
		print 'send data'
		for s in self.ccs:
			s.write(QByteArray('hi from server'))

class X(QWidget):
	def __init__(self, parent=None):
		super(X, self).__init__(parent)
		self.setWindowTitle('client')
		self.resize(200, 100)
		vbox = QVBoxLayout(self)
		self.setLayout(vbox)
		sendButton = QPushButton('send')
		sendButton.clicked.connect(self.sendData)
		vbox.addWidget(sendButton)
		recvButton = QPushButton('connect')
		recvButton.clicked.connect(self.connectX)
		vbox.addWidget(recvButton)

		self.s = QTcpSocket()
		self.s.readyRead.connect(self.readData)
		self.s.disconnected.connect(self.offline)
		self.s.error.connect(self.errorH)

		self.s.connectToHost('192.168.0.101', 8889)
	def connectX(self):
		self.s.close()
	def errorH(self, socketError):
		print 'error handle in client', socketError
	def offline(self):
		print 'server go down'
	def readData(self):
		print '-------cilent read--------'
		d = self.s.readAll()
		print d
		print '=========client read======='
	def sendData(self):
		self.s.write(QByteArray('msg from client'))

class Test(QWidget):
	def __init__(self, parent=None):
		super(Test, self).__init__(parent)
		grid = QGridLayout(self)
		self.setLayout(grid)
		s = NZFileTransfer()
		time.sleep(1)
		c = X()
		grid.addWidget(QLabel('server'), 0, 0)
		grid.addWidget(s, 0, 1)
		grid.addWidget(QLabel('client'), 1, 0)
		grid.addWidget(c, 1, 1)

import sys
a = QApplication(sys.argv)
t = Test()
t.show()
a.exec_()
