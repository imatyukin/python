#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QApplication


class Application(QApplication):

    def __init__(self):
        super().__init__(sys.argv)
