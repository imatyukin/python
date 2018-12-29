#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from queue import Queue
from http.server import HTTPServer
from .DocHandler import DocHandler


class DocServer(HTTPServer):

    def __init__(self, address):
        super().__init__(address, DocHandler)
        self.queue = Queue()
