#!/usr/bin/env python

from NZChat import NZChat
from NZQt import *

QtCore.QTextCodec.setCodecForLocale(QtCore.QTextCodec.codecForName('utf8'))
QtCore.QTextCodec.setCodecForLocale(QtCore.QTextCodec.codecForName('utf8'))
QtCore.QTextCodec.setCodecForTr(QtCore.QTextCodec.codecForName('utf8'))

if __name__ == '__main__':
	import sys
	app = QtGui.QApplication(sys.argv)
	chat = NZChat()
	chat.show()
	sys.exit(app.exec_())
