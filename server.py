#  coding: utf-8 
import SocketServer
import mimetypes
import os

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
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


class MyWebServer(SocketServer.BaseRequestHandler):
    def create_response(self, order):
        if order == 'Ok':
            if os.path.isdir(self.path):
                self.path += 'index.html'
            file = open(self.path, "r")
            filetype, encoding = mimetypes.guess_type(self.path)
            response = "HTTP/1.1 200 OK\r\nContent-Type: " + filetype + "\r\n\r\n" + file.read()
            file.close()
            #print mimetypes.guess_type(response)
            return response
        elif order == 'Bad Path':
            response = "HTTP/1.1 404 Not Found\r\n\r\n"
            return response
        else:
            response = "HTTP/1.1 405 Method Not Allowed\r\n\r\n"
            return response

    def evaluate_path(self,path):
        base_path = os.getcwd() + '/www'
        self.path = base_path + path
        #print self.path
        if '/../' in self.path:
            return 'Bad Path'
        elif os.path.exists(self.path):
            return 'Ok'
        else:
            return 'Bad Path'

    def handle(self):
        self.data = self.request.recv(1024).strip()
        print ("Got a request of: %s\n" % self.data)
        request = self.data.split()
        http_method = request[0]
        if http_method == 'GET':
            conclusion = self.evaluate_path(request[1])
        else:
            conclusion = 'Wrong Method'
        #print conclusion
        response = self.create_response(conclusion)
        self.request.sendall(response)

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    SocketServer.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = SocketServer.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
