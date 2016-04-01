#pylint: disable=E0611, w0614, R0903
#-*-coding: utf-8 -*-

import sys
import os.path
from PyQt4.QtCore import QUrl, Qt
from PyQt4.QtGui import QWidget, QSplitter, QVBoxLayout, QApplication
from plus.kiwoom import KiwoomWebViewPlus

class Window(QWidget):
    """
    main window layout
    """
    def __init__(self, entryfile):
        super().__init__()
        self.view = KiwoomWebViewPlus()
        self.view.load(QUrl(entryfile))
        self._initUI()
        
    def _initUI(self):
        layout = QVBoxLayout()
        layout.setMargin(0)
        splitter = QSplitter(Qt.Vertical)
        splitter.addWidget(self.view)
        splitter.addWidget(self.view.webInspector)
        layout.addWidget(splitter)

        self.setLayout(layout)
        self.setMinimumSize(1024, 600)
        self.setWindowTitle("QWebview-plus for Kiwoom")

        # window.view.setHtml(open(entryfle, encoding="utf8").read())

def main():
    try:
        entryfile = sys.argv[1]
    except IndexError:
        entryfile = "index.html"

    if os.path.isfile(entryfile):
        app = QApplication(sys.argv)
        window = Window(entryfile)
        window.show()
        sys.exit(app.exec_())
    else:
        sys.exit("진입 페이지를 지정해 주세요")

if __name__ == "__main__":
    main()
