#-*- coding: utf-8 -*-

from NZQt import *
from NZContact import NZContact 
from NZMessage import NZMsgType
from NZMessage import NZMessage

class NZMsgEdit(QtGui.QTextEdit):
	def __init__(self, parent=None):
		super(NZMsgEdit, self).__init__(parent)
		fragment = QtGui.QTextDocumentFragment.fromHtml('<img src="./avatar.png">')
		self.textCursor().insertFragment(fragment)
	def canInsertFromMimeData(self, source):
		if source.hasImage():
			print 'has image'
			return True
		elif source.hasUrls():
			print 'has url'
			return True
		else:
			print 'other'
			return super(NZMsgEdit, self).canInsertFromMimeData(source)
	def insertFromMimeData(self, source):
		if source.hasImage():
			print type(QtGui.QImage(source.imageData().value()))
			if source.imageData().isNull():
				print 'null image'
			else:
				print 'mimage not null'
			self.dropImage(QtCore.QUrl(QtCore.QString("dropped_image_1")), source.imageData())
		elif source.hasUrls():
			for url in source.urls():
				f = QtCore.QFileInfo(url.toLocalFile())
				if f.suffix().toLower().toLatin1() in QtGui.QImageReader.supportedImageFormats():
#				if (QtGui.QImageReader.supportedImageFormats().contains(finfo.suffix().toLower().toLatin1())):
					print 'ok , could try'
					self.dropImage(url, QtGui.QImage(f.filePath()))
				else:
					self.dropTextFile(url)
		else:
			super(NZMsgEdit, self).insertFromMimeData(source)
	def dropImage(self, url, image):
		print 'drop image with url:', url
		if not image.isNull():
			self.document().addResource(QtGui.QTextDocument.ImageResource, url, image)
			self.textCursor().insertImage(url.toString())
	def dropTextFile(self, url):
		f = QtCore.QFile(url.toLocalFile())
		if f.open(QtCore.QIODevice.ReadOnly | QtCore.QIODevice.Text):
			self.textCursor().insertText(QtCore.QString(f.readAll()))

class NZMsgView(QtGui.QTextBrowser):
	def __init__(self, parent=None):
		super(NZMsgView, self).__init__(parent)

	def insertMsg(self, msg):
		cursor = self.textCursor()
		hmsg = '<font color=blue>' + msg.hostname + ' ' + msg.time + \
		'</font><br /><font color=darkblue>' + msg.data + '</font><br />'
		cursor.insertHtml(hmsg)

class NZChatTab(QtGui.QFrame):
	def __init__(self, config, contact, parent=None):
		super(NZChatTab, self).__init__(parent)

		self.config = config
		self.contact = contact

		vbox = QtGui.QVBoxLayout(self)
		self.setLayout(vbox)
		self.msgView = NZMsgView(self)#QtGui.QTextBrowser(self)
		self.msgEdit = NZMsgEdit(self)
		vbox.addWidget(self.msgView, stretch = 7)
		vbox.addWidget(self.msgEdit, stretch = 2)
		self.clearButton = QtGui.QPushButton(self.tr('清除'))
		self.sendButton = QtGui.QPushButton(self.tr('发送'))
		hbox = QtGui.QHBoxLayout()
		hbox.addStretch()
		hbox.addWidget(self.clearButton)
		hbox.addWidget(self.sendButton)
		vbox.addLayout(hbox, stretch = 1)
		self.clearButton.clicked.connect(self.msgEdit.clear)
		self.sendButton.clicked.connect(self.sendMsg)

		self.config.chatSocket.readyRead.connect(self.recvMsg)
		self.connect(self.config.chatSocket, QtCore.SIGNAL('error(QtNetwork.QAbstractSocket.SocketError)'), QtCore.SLOT(self.displayError(QtNetwork.QAbstractSocket.SocketError)))
	def sendMsg(self):
		d = self.msgEdit.toPlainText()
		if not len(d) > 0:
			return
		msg = NZMessage(NZMsgType.TEXTMSG, data=d)
		self.msgView.insertMsg(msg)
		print 'send to:', self.contact.addr.toString()
		self.config.chatSocket.writeDatagram(msg.encode(), self.contact.addr, self.config.chatPort)
		self.msgEdit.clear()
	def recvMsg(self):
		print '--------------->recving'
		while self.config.chatSocket.hasPendingDatagrams():
			datagram, sender, port = self.config.chatSocket.readDatagram(self.config.chatSocket.pendingDatagramSize())
			msg = NZMessage.decode(datagram)
			if msg and len(msg.data) > 0:
				self.processMsg(msg)
	def processMsg(self, msg):
		print 'processing msg'
		opts = dict({
			NZMsgType.TEXTMSG:	self.processTextMsg,
		})
		if msg.mtype in opts:
			print 'can handle this'
			opts[msg.mtype](msg)
		else:
			print "can't handle this, Orz"
	def processTextMsg(self, msg):
		self.msgView.insertMsg(msg)
	def displayError(self, socketError):
		print 'error appeared'
		


class NZChatWindow(QtGui.QMainWindow):
	def __init__(self, config, parent=None):
		super(NZChatWindow, self).__init__(parent)
		self.config = config
		self.setWindowTitle(self.tr("聊天"))
		self.resize(500, 500)
		self.tabs = QtGui.QTabWidget(self)
		self.setCentralWidget(self.tabs)
		self.chatTabs = dict()
	def addChatTab(self, contact):
		if contact.addr in self.chatTabs:
			print 'in, make show'
		else:
			tab = NZChatTab(self.config, contact, self)
			self.chatTabs[contact.addr] = tab
			self.tabs.addTab(tab, contact.name)
		self.show()
