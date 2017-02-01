#!/usr/local/bin/python
# -*- coding: utf-8 -*-

from SimpleWebSocketServer import WebSocket, SimpleWebSocketServer, SimpleSSLWebSocketServer
class Ccai:
    def init(self):
        self.ws = WebSocket("ws://localhost:8000/")
        self.ws.handleConnected(self.ws)
        print (self.ws.address)

    def start(self):
        self.websocket.sendMessage(unicode("היי, נבראתי על מנת לחסוך לך זמן."))
        print ("היי, נבראתי על מנת לחסוך לך זמן.")

    def send(self):
        self.websocket.sendMessage(unicode("התחלנו."))

    def rcv(self,data):
        self.websocket.sendMessage(unicode(data + "קיבלתי."))
        Ccai.send()
