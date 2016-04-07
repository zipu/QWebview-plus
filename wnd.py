#!/usr/bin/env python
#-*-coding: utf-8 -*-
import sys
import os.path
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QSplitter, QMessageBox
from plus.kiwoom import KiwoomWebViewPlus

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(1024, 640)
        self.setWindowTitle("QWebview-plus for Kiwoom")
        self.view = KiwoomWebViewPlus()
        self.setCentralWidget(self.view)

        self.view.devTool.setVisible(True)

        # view split
        # self.splitter = QSplitter(self)
        # self.splitter.setOrientation(Qt.Horizontal)
        # layout = QVBoxLayout(self)
        # layout.setContentsMargins(0,0,0,0)
        # layout.addWidget(self.splitter)
        # self.splitter.addWidget(self.view)
        # self.splitter.addWidget(self.view.webInspector)
        # self.view.webInspector.setVisible(True)
        # self.splitter.setSizes([640,640])

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message', "Are you sure to quit?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

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
