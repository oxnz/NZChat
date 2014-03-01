""" to see all ports on windows: netstat -ap udp | find "4545" """
from PyQt4 import QtCore, QtGui, QtNetwork

unicast_addr = "127.0.0.1"
unicast_port = 45455
mcast_addr = "239.255.43.21"
mcast_port = 45454

class Sender(QtGui.QDialog):


    def processPendingDatagrams(self):
        while self.udpServer.hasPendingDatagrams():
#            datagram, host, port = self.udpServer.readDatagram(self.udpSocket.pendingDatagramSize())
            datagram, host, port = self.udpServer.readDatagram(self.udpServer.pendingDatagramSize())
            print "got msg:", datagram

    def __init__(self, parent=None):
        super(Sender, self).__init__(parent)

        self.groupAddress = QtNetwork.QHostAddress(mcast_addr)
        self.unicastAddress = QtNetwork.QHostAddress(unicast_addr)

        self.statusLabel = QtGui.QLabel("Ready to multicast datagrams to group %s on port 45454" % 
                                        self.groupAddress.toString()) 

        # setup socket for listening on incomming datagrams
        self.udpServer = QtNetwork.QUdpSocket(self)
        self.udpServer.bind(unicast_port)
        self.udpServer.readyRead.connect(self.processPendingDatagrams)

        self.startButton = QtGui.QPushButton("&Start")
        self.quitButton = QtGui.QPushButton("&Quit")

        buttonBox = QtGui.QDialogButtonBox()
        buttonBox.addButton(self.startButton, QtGui.QDialogButtonBox.ActionRole)
        buttonBox.addButton(self.quitButton, QtGui.QDialogButtonBox.RejectRole)

        self.timer = QtCore.QTimer(self)
        self.udpSocket = QtNetwork.QUdpSocket(self)
        self.messageNo = 1

        self.startButton.clicked.connect(self.startSending)
        self.quitButton.clicked.connect(self.close)
        self.timer.timeout.connect(self.send_mc_msg)

        mainLayout = QtGui.QVBoxLayout()
        mainLayout.addWidget(self.statusLabel)
        mainLayout.addWidget(buttonBox)
        self.setLayout(mainLayout)

        self.setWindowTitle("WSim")

    def startSending(self):
        self.startButton.setEnabled(False)
        self.timer.start(1000)

    def send_mc_msg(self):
        self.udpSocket.writeDatagram("hello %d" %(self.messageNo), self.groupAddress, mcast_port)
        self.messageNo += 1

if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    sender = Sender()
    sender.show()
    sys.exit(sender.exec_())
