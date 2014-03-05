#-*- coding: utf-8 -*-
from NZQt import *
from NZContactPane import NZContactPane

class NZContentPane(QtGui.QTabWidget):
	def __init__(self, config, report, parent=None):
		super(NZContentPane, self).__init__(parent)

		contactPane = NZContactPane(config, report, self)
		self.addTab(contactPane, self.tr('联系人'))
		self.addTab(QtGui.QLabel(self.tr('暂未实现')), self.tr('广播'))
		self.addTab(QtGui.QLabel(self.tr('暂未实现')), self.tr('服务'))
#		self.verticalHeader().setResizeMode(QtGui.QHeaderView.Stretch)
#		self.HorizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)
