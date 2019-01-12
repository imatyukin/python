#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QDialog, QFrame, QLineEdit
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout
from PyQt5.QtWidgets import QPushButton, QSpacerItem


class DataFrame(QFrame):

    def __init__(self, parent=None):
        super().__init__(parent)
        
        layout = QHBoxLayout(self)
        
        self.__x = QLineEdit(parent=self)
        layout.addWidget(self.__x)

        self.__y = QLineEdit(parent=self)
        layout.addWidget(self.__y)

    @property
    def x(self):
        return float(self.__x.text().strip())

    @property
    def y(self):
        return float(self.__y.text().strip())


class Dialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        
        layout = QVBoxLayout(self)
        
        self.__frame = DataFrame(parent=self)
        layout.addWidget(self.__frame)
        
        btns = QHBoxLayout()
        layout.addLayout(btns)

        ok = QPushButton(parent=self)
        ok.setText('OK')
        btns.addWidget(ok)

        cancel = QPushButton(parent=self)
        cancel.setText('Cancel')
        btns.addWidget(cancel)
        
        ok.clicked.connect(self.accept)
        cancel.clicked.connect(self.reject)
        
    @property
    def x(self):
        return self.__frame.x

    @property
    def y(self):
        return self.__frame.y
