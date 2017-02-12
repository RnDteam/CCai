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

        # Analyze parameters
        if self.path.find('?') > -1:
            pathParams = self.path.split("?")[1]
            paramDic = self.CreateParamDic(pathParams)

        client_ip = self.getUrl(paramDic)

        if client_ip not in USERS:
            USERS[client_ip] = User.User(client_ip)

        # Write content as utf-8 data
        str_first_buttons = '[בוא נתחיל|תדריך אותי]'
        self.wfile.write("נעים להכיר, אני combot שיודע לעזור לך לפתור תקלות בצורה פשוטה וכייפית.\nאני חדש כאן ולא יודע לענות על כל דבר, אבל מיום ליום אני הולך ומשתדרג!\nאני רואה שגם אתה חדש כאן! תרצה הדרכה קצרה על איך משתמשים בי?\n".encode("utf-8"))
        self.wfile.write(str_first_buttons.encode("utf-8"))
        #self.wfile.write("תוכל לפנות אליי במלל חופשי ואנסה להבין כיצד לסייע לך :)".encode("utf-8"))
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
        if len(message) > 0:
            user_message = User.UserMessage(USERS[self.getUrl(paramDic)], message)
            self.wfile.write(bytes(hebChatbot.Start(user_message), "utf-8"))
        else:
            self.wfile.write(bytes('?', "utf-8"))
    def getUrl(self, paramDic):
        client_ip = paramDic["client_ip"]
        port = paramDic["port"]
        return client_ip + ":" + str(port)

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
    server_address = ('127.0.0.1', 8082)
    httpd = HTTPServer(server_address, MyRequestHandler)
    print('running server...')
    httpd.serve_forever()

run()