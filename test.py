#!/usr/bin/env python

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from NZChat import NZChat

if __name__ == '__main__':
	import sys
	app = QApplication(sys.argv)
	chat = NZChat()
	chat.show()
	sys.exit(app.exec_())
