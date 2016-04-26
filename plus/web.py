# -*-coding: utf-8 -*-

import logging
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from PyQt5.QtWidgets import QShortcut
from PyQt5.QtCore import Qt


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
        shortcut = {}

        #F5 - Page reloading
        shortcut['F5'] = QShortcut(self)
        shortcut['F5'].setKey(Qt.Key_F5)
        shortcut['F5'].activated.connect(self.reload)


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
