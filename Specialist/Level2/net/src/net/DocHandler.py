#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pickle
from http.server import BaseHTTPRequestHandler


class DocHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        print('GET request handled')

    def do_POST(self):
        size = int(self.headers['Content-length'])
        data = self.rfile.read(size)
        data = pickle.loads(data)
        print(data)
        data.append(1)
        data = pickle.dumps(data)
        self.send_response(200, 'OK')
        self.end_headers()
        self.wfile.write(data)
