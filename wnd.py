#pylint: disable=E0611, w0614, R0903
#-*-coding: utf-8 -*-
import sys
import os.path
from optparse import OptionParser
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from plus.kiwoom import KiwoomWebViewPlus

class Window(QMainWindow):
    """
    main window layout
    """
    def __init__(self):
        super().__init__()
        self.view = KiwoomWebViewPlus()
        self.setCentralWidget(self.view)
        self.setMinimumSize(1200, 800)
        self.setWindowTitle("QWebview-plus for Kiwoom")

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message', "Are you sure to quit?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

def main():
    #command line argument parsing
    parser = OptionParser()
    parser.add_option("--remote-debugging-port", action="store", type="string", dest="port")
    (opt, arg) = parser.parse_args()

    if (len(arg) > 0):
        entryfile = arg[0]
    else:
        entryfile = "index.html"

    if os.path.isfile(entryfile):
        app = QApplication(sys.argv)
        window = Window()
        window.view.load(QUrl.fromLocalFile(os.path.join(os.path.dirname( os.path.abspath( __file__ ) ), entryfile)))
        
        #--remote-debugging-port 옵션 있을 시 Dev Tool("F12" 키) 활성화
        #cross-origin 문제 있음..
        if  opt.port is not None:
            window.view.debuggingMode(opt.port)
        window.show()
        sys.exit(app.exec_())
    else:
        sys.exit("진입 페이지를 지정해 주세요")

if __name__ == "__main__":
    main()
