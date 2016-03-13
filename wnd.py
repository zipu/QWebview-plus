#-*-coding: utf-8 -*-
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import QWidget, QSplitter, QVBoxLayout, QApplication
from plus.web import KiwoomWebViewPlus

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.view = KiwoomWebViewPlus()
        self.splitter = QSplitter(self)
        self.splitter.setOrientation(Qt.Vertical)
        layout = QVBoxLayout(self)
        layout.setMargin(0)
        layout.addWidget(self.splitter)
        self.splitter.addWidget(self.view)
        self.splitter.addWidget(self.view.webInspector)

def main():
    app = QApplication(sys.argv)
    window = Window()
    window.view.setHtml(open(sys.argv[1]).read())
    window.show()
    app.exec_()

if __name__ == "__main__":
    main()