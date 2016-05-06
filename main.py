#!/usr/bin/env python
#-*-coding: utf-8 -*-
import sys
import os.path
import configparser
from optparse import OptionParser
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from plus.kiwoom import KiwoomWebViewPlus

class Window(QMainWindow):
    def __init__(self, port=None):
        super().__init__()
        self.setMinimumSize(680,480)
        self.setWindowTitle("QWebview-plus for Kiwoom")
        self.view = KiwoomWebViewPlus()
        self.setCentralWidget(self.view)
        if port is not None:
            self.view.debuggingMode(port)

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message', "Are you sure to quit?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

if __name__ == "__main__":
    #parsing command line arguments
    parser = OptionParser()
    parser.add_option("-p", "--port", action="store", type="string", dest="port", help="크롬 원격 디버깅 포트")
    parser.add_option("-f", "--file", action="store", type="string", dest="file", help="시작 파일 경로", default="./index.html")
    (opt, args) = parser.parse_args()

    if os.path.isfile(opt.file):
        # application 이 실행하기 전에 port 가 처리되어야 한다.
        if opt.port is not None:
            os.environ["QTWEBENGINE_REMOTE_DEBUGGING"] = "0.0.0.0:" + str(opt.port)

        app = QApplication(sys.argv)
        window = Window(opt.port)
        window.view.load(QUrl.fromLocalFile(os.path.join(os.path.dirname( os.path.abspath( __file__ ) ), opt.file)))
        #if opt.port is not None:
        #    window.view.debuggingMode(opt.port)
        window.show()
        sys.exit(app.exec_())
    else:
        parser.print_help()
        sys.exit()
