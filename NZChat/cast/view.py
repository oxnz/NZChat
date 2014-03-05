#!/usr/bin/python

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtNetwork import *
import socket
import sys
import time

class NZView(QWidget):
	def __init__(self, parent=None):
		super(NZView,  self).__init__(parent)
		self.resize(600, 400)
		vbox = QVBoxLayout(self)
		self.setLayout(vbox)

		self.textView = QTextBrowser(self)
		self.textEdit = QTextEdit(self)
		self.commitButton = QPushButton("commit")
		self.commitButton.clicked.connect(self.commitText)

		vbox.addWidget(self.textView)
		vbox.addWidget(self.textEdit)
		vbox.addWidget(self.commitButton)

		self.document = self.textView.document()
		self.cursor = self.textView.textCursor()
		self.fileButton = QPushButton("Send File")
		self.fileButton.clicked.connect(self.sendFile)
		vbox.addWidget(self.fileButton)
	def commitText(self):
		txt = self.textEdit.toPlainText()
		self.cursor.beginEditBlock()
		for i in range(len(txt)):
			self.cursor.insertText(txt[i])
		self.cursor.insertBlock();
		self.cursor.endEditBlock()
	def sendFile(self):
		print 'sending file'
		f = QFileDialog.getOpenFileName(self,
				self.tr("select an image"),
				".",
				self.tr("Bitmap Files (*.bmp)\nJPEG (*.jpg *.jpeg)\nGIF (*.gif)\nPNG (*.png)\nall (*.*)"))
		if f == '':
			return
		url = QUrl(QString("file://%1").arg(f))
		image = QImageReader(f).read()
		textDocument = self.textEdit.document()
		textDocument.addResource(QTextDocument.ImageResource, url, QVariant(image))
		imageFormat = QTextImageFormat()
		imageFormat.setWidth(image.width())
		imageFormat.setHeight(image.height())
		imageFormat.setName(url.toString())
		self.textEdit.textCursor().insertImage(imageFormat)


app = QApplication(sys.argv)
x = NZView()
x.show()
app.exec_()
