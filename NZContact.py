#-*- coding: utf-8 -*-

from NZQt import *

class NZContact(QtGui.QToolButton):
	def __init__(self, config, addChatTab, IP, name = 'Anonymous', parent=None):
		super(NZContact, self).__init__(parent)

		self.config = config
		self.__name = name
		self.__addr = QtNetwork.QHostAddress(IP)

		self.setText(str(name) + '\n' + str(IP))
		self.setIcon(QtGui.QIcon('./avatar.png'))
		self.setIconSize(QtCore.QSize(80, 80))
		self.setAutoRaise(True)
		self.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)

		self.clicked.connect(self.chatWith)

		self.addChatTab = addChatTab
	@property
	def name(self):
		return self.__name
	@property
	def addr(self):
		return self.__addr
	def chatWith(self):
		self.addChatTab(self)
	def offline(self):
		print 'go offline'
