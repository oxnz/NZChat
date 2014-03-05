#!/usr/bin/env python

from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys
import json
import time

class NZChat(QWidget):
	class Header(QWidget):
		def __init__(self, parent):
			super(parent.Header, self).__init__(parent)
			print 'init header'
	def __init__(self):
		super(NZChat, self).__init__(None)
		print 'init chat'
		vbox = QVBoxLayout(self)
		h = self.Header(self)
		vbox.addWidget(h)

if __name__ == '__main__':
	app = QApplication(sys.argv)
	ui = NZChat()
	ui.show()
	sys.exit(app.exec_())
