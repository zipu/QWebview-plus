#pylint: disable=E0611, w0614, R0903
#-*-coding: utf-8 -*-

import sys
import os.path
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication, QMainWindow, QStatusBar, QMessageBox, QVBoxLayout, QSplitter, QTextEdit
from plus.kiwoom import KiwoomWebViewPlus


class Window(QMainWindow):
    """
    main window layout
    """
    def __init__(self):
        super().__init__()
        self.view = KiwoomWebViewPlus()
        self.initUI()

    def initUI(self):
        self.setCentralWidget(self.view)
        self.setMinimumSize(1024, 600)
        self.setWindowTitle("QWebview-plus for Kiwoom")

        self.view.statusbar = QStatusBar()
        self.setStatusBar(self.view.statusbar)
        self.view.statusbar.showMessage("Press 'F12' button to open development tool")

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message', "Are you sure to quit?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

def main():
    try:
        entryfile = sys.argv[1]
    except IndexError:
        entryfile = "index.html"

    if os.path.isfile(entryfile):
        app = QApplication(sys.argv)
        window = Window()
        window.view.load(QUrl.fromLocalFile(os.path.join(os.path.dirname( os.path.abspath( __file__ ) ), entryfile)))
        window.show()
        sys.exit(app.exec_())
    else:
        sys.exit("진입 페이지를 지정해 주세요")

if __name__ == "__main__":
    main()
