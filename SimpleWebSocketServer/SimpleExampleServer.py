#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
The MIT License (MIT)
Copyright (c) 2013 Dave P.
'''

import requests
import signal
import sys
import ssl
from SimpleWebSocketServer import WebSocket, SimpleWebSocketServer, SimpleSSLWebSocketServer
from optparse import OptionParser

class SimpleEcho(WebSocket):

   def handleMessage(self):
      self.sendMessage(self.data)

   def handleConnected(self):
      pass

   def handleClose(self):
      pass

clients = []
DOMAIN = "localhost"
PORT = 8082
CHATBOT_URL = 'http://' + DOMAIN + ":" + str(PORT)

class SimpleChat(WebSocket):

   def handleMessage(self):
      for client in clients:
         if client.address[1] == self.address[1]:
            try:
               r = requests.post(CHATBOT_URL, json= { "message": self.data }, params={"client_ip": self.address[0], "port": self.address[1]})
               client.sendMessage(r.text)
            except Exception as e:
               print(e)

   def handleConnected(self):
      print (self.address, 'connected')
      try:
         # TODO senging port only because we're checking it in one computer
         #      and that's how we distinguish between users. On prod only ip would be fine
         r = requests.get(CHATBOT_URL, params={"client_ip": self.address[0], "port": self.address[1]})
         self.sendMessage(r.text)
      except Exception as e:
         print(e)
      clients.append(self)

   def handleClose(self):
      clients.remove(self)
      print (self.address, 'closed')


if __name__ == "__main__":

   parser = OptionParser(usage="usage: %prog [options]", version="%prog 1.0")
   parser.add_option("--host", default='', type='string', action="store", dest="host", help="hostname (localhost)")
   parser.add_option("--port", default=8000, type='int', action="store", dest="port", help="port (8000)")
   parser.add_option("--example", default='echo', type='string', action="store", dest="example", help="echo, chat")
   parser.add_option("--ssl", default=0, type='int', action="store", dest="ssl", help="ssl (1: on, 0: off (default))")
   parser.add_option("--cert", default='./cert.pem', type='string', action="store", dest="cert", help="cert (./cert.pem)")
   parser.add_option("--ver", default=ssl.PROTOCOL_TLSv1, type=int, action="store", dest="ver", help="ssl version")

   (options, args) = parser.parse_args()
   cls = SimpleChat

   if options.ssl == 1:
      server = SimpleSSLWebSocketServer(options.host, options.port, cls, options.cert, options.cert, version=options.ver)
   else:
      server = SimpleWebSocketServer(options.host, options.port, cls)

   def close_sig_handler(signal, frame):
      server.close()
      sys.exit()

   signal.signal(signal.SIGINT, close_sig_handler)

   server.serveforever()
