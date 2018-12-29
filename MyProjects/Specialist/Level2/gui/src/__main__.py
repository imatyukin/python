#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from Application import Application
from MainWindow import MainWindow

app = Application()

main_window = MainWindow()
main_window.showMaximized()

result = app.exec_()
sys.exit(result)
