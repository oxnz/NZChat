""" to see all ports on windows: netstat -ap udp | find "4545" """
from PyQt4 import QtCore, QtGui, QtNetwork

class Sender(QtGui.QWidget):
    def processPendingDatagrams(self):
        while self.udpServer.hasPendingDatagrams():
            datagram, host, port = self.udpServer.readDatagram(self.udpServer.pendingDatagramSize())
            print "got msg: %s from %s %s" % (datagram, host.toString(), port)

    def __init__(self, parent=None):
        super(Sender, self).__init__(parent)
        # setup socket for listening on incomming datagrams
        self.udpServer = QtNetwork.QUdpSocket(self)
        self.udpServer.bind(8888)
        self.udpServer.readyRead.connect(self.processPendingDatagrams)

if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    sender = Sender()
    sender.show()
    sys.exit(app.exec_())
