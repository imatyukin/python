#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pickle
from http.server import BaseHTTPRequestHandler


class DocHandler(BaseHTTPRequestHandler):

    def do_POST(self):
        try:
            print(self.path)
            size = int(self.headers['Content-length'])
            data = self.rfile.read(size)
            data = pickle.loads(data)
            self.server.queue.put(data)
            self.send_response(200, 'OK')
            self.end_headers()
            self.wfile.write('OK'.encode('utf-8'))
        except:
            self.send_response(400, 'Bad request')
            self.end_headers()
            raise
