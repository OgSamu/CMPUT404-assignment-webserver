#  coding: utf-8 
import socketserver

# Copyright 2013 Abram Hindle, Eddie Antonio Santos, Urvi Patel
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/

# Constants
BASE_PATH = "./www"
HTML_TYPE = "text/html"
CSS_TYPE = "text/css"
HTTP_OK = "HTTP/1.1 200 OK"
HTTP_NOT_FOUND = "HTTP/1.1 404 Not Found"
HTTP_NOT_ALLOWED = "HTTP/1.1 405 Method Not Allowed"
HTTP_MOVED = "HTTP/1.1 301 Moved Permanently"
CONNECTION_CLOSE = "Connection: close"
ERROR_HTML = "<html><body><h1>{}</h1></body></html>"  # useful for user for error message 


class MyWebServer(socketserver.BaseRequestHandler):

    def handle(self):
        self.data = self.request.recv(1024).strip()
        cleanSplit = self.data.decode().split("\r\n")
        data = cleanSplit[0].split(" ")
        method = data[0]
        path = data[1]

        if method == "GET":
           response = self.handle_get(path)
        else:
            response = HTTP_NOT_ALLOWED + "\r\n"

        self.request.sendall(bytearray(response, 'utf-8'))
        return
    
    def handle_get(self, path):
        if path.endswith(".css"):
            response = self.get_cssRes(path)
        elif path.endswith("/"):
            response = self.get_indexRes(path)
        elif path.endswith(".html"):
            response = self.get_htmlRes(path)
        elif path.startswith("/.."):
            response = HTTP_NOT_FOUND + "\r\n"
        else:
            response = self.redirect_index(path)
        return response

    def get_indexRes(self, path):
        fname = BASE_PATH + path + "index.html"
        try:
            content = self.rFile(fname)
            response = "{}\r\nContent-Type: {}\r\n\r\n{}".format(HTTP_OK, HTML_TYPE, content)
        except:
            response = HTTP_NOT_FOUND + "\r\n"
        return response

    def get_htmlRes(self, path):
        fname = BASE_PATH + path
        try:
            content = self.rFile(fname)
            response = "{}\r\nContent-Type: {}\r\n\r\n{}".format(HTTP_OK, HTML_TYPE, content)
        except:
            response = HTTP_NOT_FOUND + "\r\n"
        return response

    def get_cssRes(self, path):
        fname = BASE_PATH + path
        try:
            content = self.rFile(fname)
            response = "{}\r\nContent-Type: {}\r\n\r\n{}".format(HTTP_OK, CSS_TYPE, content)
        except:
            response = HTTP_NOT_FOUND + "\r\n"
        return response

    def redirect_index(self, path):
        fname = BASE_PATH + path + "/index.html"
        try:
            content = self.rFile(fname)
            response = "{}\r\nLocation: {}\r\n".format(HTTP_MOVED, path + "/")
        except:
            response = HTTP_NOT_FOUND + "\r\n"
        return response

    def rFile(self, name):
        with open(name, "r") as f:
            content = f.read()
        return content

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()