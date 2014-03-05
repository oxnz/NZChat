from PyQt4 import QtGui, QtNetwork

mcast_addr = "239.255.43.21"
mcast_port = 45454
answer_addr = "127.0.0.1"
answer_port = 45455

class Receiver(QtGui.QDialog):
    def __init__(self, parent=None):
        super(Receiver, self).__init__(parent)

        self.groupAddress = QtNetwork.QHostAddress(mcast_addr)        
        self.udpSocket = QtNetwork.QUdpSocket(self)
        self.udpSocket.bind(mcast_port, QtNetwork.QUdpSocket.ReuseAddressHint)
        self.udpSocket.joinMulticastGroup(self.groupAddress)
        self.udpSocket.readyRead.connect(self.processPendingDatagrams)

        # Use this socket to send unicast messages to back
        self.answerSocket = QtNetwork.QUdpSocket(self)
        self.answerAddress = QtNetwork.QHostAddress(answer_addr)        

        quitButton = QtGui.QPushButton("&Quit")
        quitButton.clicked.connect(self.close)

        buttonLayout = QtGui.QHBoxLayout()
        buttonLayout.addStretch(1)
        buttonLayout.addWidget(quitButton)
        buttonLayout.addStretch(1)

        self.statusLabel = QtGui.QLabel("Listening for multicasted messages on %s" % mcast_addr) 
        mainLayout = QtGui.QVBoxLayout()
        mainLayout.addWidget(self.statusLabel)
        mainLayout.addLayout(buttonLayout)
        self.setLayout(mainLayout)

        self.setWindowTitle("mrecv")

    def processPendingDatagrams(self):
        """receive and decode multicast messages and send a response message on the return address"""

        while self.udpSocket.hasPendingDatagrams():
            datagram, host, port = self.udpSocket.readDatagram(self.udpSocket.pendingDatagramSize())
            self.statusLabel.setText("received mcast msg '%s'" % datagram)
            # send a response back to msend 
            self.answerSocket.writeDatagram("hi back", self.answerAddress, answer_port)

if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    receiver = Receiver()
    receiver.show()
    sys.exit(receiver.exec_())