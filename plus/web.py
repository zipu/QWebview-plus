# -*-coding: utf-8 -*-
import logging
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from PyQt5.QtWidgets import QShortcut, QDialog, QGridLayout
from PyQt5.QtCore import Qt, QUrl
from optparse import OptionParser


class WebViewPlus(QWebEngineView):
    """
	WebView 커스터마이징
	 - inspector 추가
	 - jsconsole 로그 추가
	 - webview에서 document로 이벤트를 발생함.
	"""

    def __init__(self):
        super().__init__()
        self.setPage(WebPagePlus())


        #Keyboard shortcuts
        self.shortcut = {}

        #F5 - Page reloading
        self.shortcut['F5'] = QShortcut(self)
        self.shortcut['F5'].setKey(Qt.Key_F5)
        self.shortcut['F5'].activated.connect(self.reload)

    #Devtool setup
    def debuggingMode(self, port):
        #F12 - Development tool
        self.shortcut['F12'] = QShortcut(self)
        self.shortcut['F12'].setContext(Qt.ApplicationShortcut)
        self.shortcut['F12'].setKey(Qt.Key_F12)
        self.shortcut['F12'].activated.connect(self._toggleDevTool)

        self.devTool = QDialog(self)
        self.devTool.setWindowTitle("Development Tool")
        self.devTool.resize(950, 400)

        self.devView = QWebEngineView()
        self.devView.setPage(QWebEnginePage(self.devView))
        
        self.devView.load(QUrl("http://localhost:"+port))
        layout = QGridLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.devView)
        self.devTool.setLayout(layout)

    def _toggleDevTool(self):
        """
        F12키를 다시 누르면 "개발자 도구"가 사라짐
        """
        self.devTool.setVisible(not self.devTool.isVisible())

class WebPagePlus(QWebEnginePage):
    """
	javascript 콘솔 메시지를 python logger에 출력
	http://pyqt.sourceforge.net/Docs/PyQt4/qwebpage.html
	"""

    def __init__(self, logger=None):
        super().__init__()
        if not logger:
            logger = logging
        self.logger = logger

    def javaScriptConsoleMessage(self, level, msg, lineNumber, sourceID):
        self.logger.warning("console(%s:%d): %s" % (sourceID, lineNumber, msg))
