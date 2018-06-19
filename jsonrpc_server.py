#!/usr/bin/env python
# coding: utf-8

import pyjsonrpc
from time import sleep

class RequestHandler(pyjsonrpc.HttpRequestHandler):

    @pyjsonrpc.rpcmethod
    def add(self, a, b):
        """Test method"""
        #sleep(10)
        print "a=%d, b=%d" % (a, b)
        return a + b


# Threading HTTP-Server
http_server = pyjsonrpc.ThreadingHttpServer(
    server_address = ('127.0.0.1', 8668),
    RequestHandlerClass = RequestHandler
)
print "Starting HTTP server ..."
print "URL: http://127.0.0.1:8668"
http_server.serve_forever()

