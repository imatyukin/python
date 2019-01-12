#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QTableView
from PyQt5.QtCore import Qt, QAbstractTableModel


class Model(QAbstractTableModel):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.__xy = [
            ( 0.0,  0.0 ),
            ( 1.0,  1.0 ),
            ( 2.0,  4.0 ),
            ( 3.0,  9.0 ),
            ( 4.0, 16.0 ),
            ( 5.0, 25.0 ),
        ]
        
    def columnCount(self, parentIndex=None):
        return 2
        
    def rowCount(self, parentIndex=None):
        return len(self.__xy)
        
    def data(self, index, role):
        if role == Qt.DisplayRole:
            row = index.row()
            col = index.column()
            return self.__xy[row][col]
        return None
        
        
class View(QTableView):

    def __init__(self, parent=None):
        super().__init__(parent)
        model = Model(parent=self)
        self.setModel(model)
