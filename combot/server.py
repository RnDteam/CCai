#!/usr/bin/env python
# -*- coding: utf-8 -*-

from http.server import BaseHTTPRequestHandler, HTTPServer
import simplejson
from combot.conversation_reader import Conversation

clients = {}
# HTTPRequestHandler class
class MyRequestHandler(BaseHTTPRequestHandler):

    def build_msg(self):
        # Send response status code
        self.send_response(200)

        # Send headers
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    # GET
    def do_GET(self):
        self.build_msg()

    # POST
    def do_POST(self):
        self.build_msg()
        data_json = self.rfile.read(int(self.headers['Content-Length']))
        data = simplejson.loads(data_json)
        client = data['client_ip'],data['port']

        conversation = None
        if client in clients.keys():
            conversation = clients.get(client)
        else:
            conversation = Conversation()
            clients[client] = conversation
        if 'message' in data.keys():
            answer = conversation.answer(data['message'])
        else:
            answer = conversation.get_node_answer()
        self.wfile.write(bytes(answer, "utf-8"))

def run():
    print("preparing chatbot...")

    print('starting server...')

    # Server settings
    # Choose port 8080, for port 80, which is normally used for a http server, you need root access
    server_address = ('127.0.0.1', 8082)
    httpd = HTTPServer(server_address, MyRequestHandler)
    print('running server...')
    httpd.serve_forever()

run()