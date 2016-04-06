#!/usr/bin/env python
#-*-coding: utf-8 -*-
import sys
import os.path
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QWidget, QSplitter, QVBoxLayout, QApplication
from plus.kiwoom import KiwoomWebViewPlus

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(1280, 768)
        self.setWindowTitle("QWebview-plus for Kiwoom")
        self.view = KiwoomWebViewPlus()
        self.splitter = QSplitter(self)
        self.splitter.setOrientation(Qt.Horizontal)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0,0,0,0)
        layout.addWidget(self.splitter)
        self.splitter.addWidget(self.view)
        self.splitter.addWidget(self.view.webInspector)
        self.splitter.setSizes([640,640])

if __name__ == "__main__":
    if len(sys.argv) < 2:
        entryfle = "index.html" if os.path.isfile("index.html") else ""
    else:
        entryfle = sys.argv[1]

    if entryfle:
        app = QApplication(sys.argv)
        window = Window()
        window.view.load(QUrl.fromLocalFile(os.path.join(os.path.dirname( os.path.abspath( __file__ ) ), entryfle)))
        window.show()
        sys.exit(app.exec_())
    else:
        sys.exit("진입 페이지를 지정해 주세요")
