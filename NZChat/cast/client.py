#!/usr/bin/python

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtNetwork import *
import socket
import sys
import time

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
		recvButton = QPushButton('recv')
		recvButton.clicked.connect(self.readData)
		vbox.addWidget(recvButton)

		self.s = QTcpSocket()
		self.s.readyRead.connect(self.readData)
		self.s.disconnected.connect(self.offline)
		self.s.error.connect(self.errorH)

		self.s.connectToHost('192.168.0.101', 8889)
	def errorH(self):
		print 'error handle in client'
	def offline(self):
		print 'server go down'
	def readData(self):
		print '-------cilent read--------'
		d = self.s.readAll()
		print d
		print '=========client read======='
	def sendData(self):
		self.s.write(QByteArray('msg from client'))

import sys
a = QApplication(sys.argv)
t = X()
t.show()
a.exec_()
