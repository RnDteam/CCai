#!/usr/bin/env python
# -*- coding: utf-8 -*-

from http.server import BaseHTTPRequestHandler, HTTPServer
import User
import hebChatbot
import simplejson

USERS = {}

# HTTPRequestHandler class
class MyRequestHandler(BaseHTTPRequestHandler):
    # GET
    def do_GET(self):
        # Send response status code
        self.send_response(200)

        # Send headers
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        # Send message back to client
        client_ip = self.path.split("client_ip=")[1]
        client_ip = client_ip.replace("&", "")
        if client_ip not in USERS:
            USERS[client_ip] = User.User(client_ip)

        # Write content as utf-8 data
        self.wfile.write("שלום".encode("utf-8"))
        return

    def do_POST(self):
        # Send response status code
        self.send_response(200)

        # Send headers
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.data_string = self.rfile.read(int(self.headers['Content-Length']))

        data = simplejson.loads(self.data_string)
        message = data['message']
        print(message)

        curUser = User.UserMessage(USERS[self.address_string()], message)

        answer = hebChatbot.Start(curUser)

        self.wfile.write(bytes(hebChatbot.Start(curUser), "utf-8"))
        # print(hebChatbot.Start(curUser))
        print(self.address_string())

def run():
    print("preparing chatbot...")
    hebChatbot.InitEntities()

    print('starting server...')

    # Server settings
    # Choose port 8080, for port 80, which is normally used for a http server, you need root access
    server_address = ('127.0.0.1', 8081)
    httpd = HTTPServer(server_address, MyRequestHandler)
    print('running server...')
    httpd.serve_forever()

run()