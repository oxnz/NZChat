#!/usr/bin/env python
import socket

def tcpClient():
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind(('192.168.0.101', 8889))
	s.listen(10)
	while True:
		c, a = s.accept()
		print 'got connection from', a
		c.send('hello, this is server')
		r = c.recv(400)
		print 'read to server', r
		c.send('hello again, this is server')
		r = c.recv(400)
		print 'read to serv again er', r


tcpClient()
