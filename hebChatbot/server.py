#!/usr/bin/env python
# -*- coding: utf-8 -*-
from http.server import BaseHTTPRequestHandler, HTTPServer
from User import User, UserMessage
import libs.mimetypes
import hebChatbot
import simplejson
import codecs

USERS = {}

# HTTPRequestHandler class
class MyRequestHandler(BaseHTTPRequestHandler):
    # GET
    def do_GET(self):
        # Send response status code
        self.send_response(200)

        # Send headers
        self.end_headers()

        # In case the user load the page
        if self.path == '/':
            self.send_header('Content-type', 'text/html')
            self.path = "../chatUI/index.html"
            f = codecs.open(self.path, 'r', 'utf-8')
            htmlFile = f.read()
            self.wfile.write(htmlFile.encode("utf-8"))
        else:
            # TODO find a way for detecting a file requests in a more scalable way
            if self.path.find("client_ip") > -1 and self.path.find('?') > -1:
                self.send_header('Content-type', 'text/html')

                pathParams = self.path.split("?")[1]
                paramDic = self.CreateParamDic(pathParams)

                client_ip = self.getUrl(paramDic)

                if client_ip not in USERS:
                    USERS[client_ip] = User(client_ip)

                # Write content as utf-8 data
                self.wfile.write("שלום".encode("utf-8"))
            else:
                try:
                    file_type = libs.mimetypes.overwrite_mimetypes_answer(self.path)

                    if file_type is None:
                        file_type = libs.mimetypes.guess_type(self.path, strict=True)[0]

                    # Check if file type was found
                    if file_type is not None:
                        print(self.path + " , " + file_type)
                        self.send_header('Content-type', file_type)
                        # Check if the file is an image which is already encoded
                        if file_type.find("jpeg") > -1 or file_type.find("png") > -1:
                            f = open("../chatUI/" + self.path, 'rb')
                            response = f.read()
                        else:
                            f = codecs.open("../chatUI/" + self.path, 'r', 'utf-8')
                            response = f.read().encode("utf-8")

                        self.wfile.write(response)
                except OSError:# Analyze parameters
                    print(OSError)

        return

    def do_POST(self):
        # Send response status code
        self.send_response(200)

        # Send headers
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.data_string = self.rfile.read(int(self.headers['Content-Length']))

        # Analyze parameters
        if self.path.find('?') > -1:
            pathParams = self.path.split("?")[1]
            paramDic = self.CreateParamDic(pathParams)

        data = simplejson.loads(self.data_string)
        message = data['message']
        print(message)

        user_message = UserMessage(USERS[self.getUrl(paramDic)], message)

        self.wfile.write(bytes(hebChatbot.hebChatbot.Start(user_message), "utf-8"))

        return

    def getUrl(self, paramDic):
        client_ip = paramDic["client_ip"]
        port = paramDic["port"]
        return client_ip + ":" + str(port)

    # TODO - prevent false abuse of post requests by sending some unexpected params
    def CreateParamDic(self, path):
        paramsDic = {}

        pathParams = path.split("&")
        for param in pathParams:
            val = param.split("=")
            paramsDic[val[0]] = val[1]

        return paramsDic

def run():
    print("preparing chatbot...")
    hebChatbot.InitEntities()

    print('starting server...')

    # Server settings
    # Choose port 8080, for port 80, which is normally used for a http server, you need root access
    server_address = ('localhost', 8082)
    httpd = HTTPServer(server_address, MyRequestHandler)
    print('running server...')
    httpd.serve_forever()

run()