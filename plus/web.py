# -*-coding: utf-8 -*-

import logging
from PyQt4.QtWebKit import QWebView, QWebPage, QWebInspector, QWebSettings
from PyQt4.QtGui import QShortcut, QDialog, QGridLayout
from PyQt4.QtCore import Qt


class WebViewPlus(QWebView):
    """
	WebView 커스터마이징
	 - inspector 추가
	 - jsconsole 로그 추가
	 - webview에서 document로 이벤트를 발생함.
	"""

    customEvent = """
    var scope = angular.element(document.querySelector("#trading-view")).scope()
    scope.$apply(function(){{
        scope.$broadcast("{type}",{detail});
    }});
    """

    def __init__(self):
        super().__init__()
        self.setPage(WebPagePlus())
        self._setupInspector()

        #Keyboard shortcuts
        shortcut = {}

        shortcut['F12'] = QShortcut(self)
        shortcut['F12'].setContext(Qt.ApplicationShortcut)
        shortcut['F12'].setKey(Qt.Key_F12)
        shortcut['F12'].activated.connect(self._toggleInspector)

        #F5 - Page reloading
        shortcut['F5'] = QShortcut(self)
        shortcut['F5'].setKey(Qt.Key_F5)
        shortcut['F5'].activated.connect(self.reload)


    def _setupInspector(self):
        """
		F12키를 누르면 "개발자 도구"가 노출됨
		"""
        self.settings().setAttribute(QWebSettings.DeveloperExtrasEnabled, True)
        self.webInspector = QWebInspector(self)
        self.webInspector.setPage(self.page())
        self.webInspector.setVisible(True)

        self.devTool = QDialog(self)
        self.devTool.setWindowTitle("Development Tool")
        self.devTool.resize(950, 400)
        layout = QGridLayout()
        layout.addWidget(self.webInspector)
        layout.setMargin(0)
        self.devTool.setLayout(layout)


    def _toggleInspector(self):
        """
		F12키를 다시 누르면 "개발자 도구"가 사라짐
		"""
        self.devTool.setVisible(not self.devTool.isVisible())
        self.devTool.resize(950, 400)
       

    # webview의 document에 이벤트를 발생함.
    def fireEvent(self, type, detail):
        self.page().mainFrame().evaluateJavaScript(WebViewPlus.customEvent.format(type=type, detail=detail))


class WebPagePlus(QWebPage):
    """
	javascript 콘솔 메시지를 python logger에 출력
	http://pyqt.sourceforge.net/Docs/PyQt4/qwebpage.html
	"""

    def __init__(self, logger=None):
        super().__init__()
        if not logger:
            logger = logging
        self.logger = logger

    def javaScriptConsoleMessage(self, msg, lineNumber, sourceID):
        self.logger.warning("console(%s:%d): %s" % (sourceID, lineNumber, msg))