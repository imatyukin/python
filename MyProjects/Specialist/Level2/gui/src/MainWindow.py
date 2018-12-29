#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QMainWindow, QDockWidget, QFrame
from PyQt5.QtCore import Qt
import Points
import NewPoint


class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)

        dock = QDockWidget(parent=self)
        self.__points_view = pv = Points.View(parent=dock)
        dock.setWidget(pv)
        self.addDockWidget(Qt.LeftDockWidgetArea, dock)

        frame = QFrame(parent=self)
        self.setCentralWidget(frame)
        
        ap = self.menuBar().addAction('Add')
        ap.triggered.connect(self.add_point)

    def add_point(self):
        dialog = NewPoint.Dialog(self)
        result = dialog.exec_()
        if result == NewPoint.Accepted:
            # тут добавить точку
            pass
    
