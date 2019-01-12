#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from threading import Thread
from net import DocServer

class DocServerThread(Thread):

    def __init__(self, server, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__server = server

    def run(self):
        self.__server.serve_forever()

server = DocServer(('',8000))
thread = Thread(target=server.serve_forever)
thread.start()

input('Нажмите ENTER для завершения')
server.shutdown()
thread.join()
