#-*- coding: utf-8 -*-
from NZQt import *

class NZStatus(QtCore.QObject):
	'''represent user status
	there's three so far, and only 2 usable
	'''
	ONLINE = 0x00
	OFFLINE = 0x01
	INVISIBLE = 0x02
