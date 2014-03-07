from PyQt4.QtCore import *
from PyQt4.QtGui import *

class NZSettings(QWidget):
	def __init__(self, parent):
		super(NZSettings, self).__init__(parent)
		self.account.nickname = QString('me')
