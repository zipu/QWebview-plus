#-*-coding: utf-8 -*-
import logging
from PyQt4.QtWebKit import QWebView, QWebPage, QWebInspector, QWebSettings
from PyQt4.QtGui import QShortcut
from PyQt4.QtCore import Qt

class WebViewPlus(QWebView):
    """
    WebView 커스터마이징
     - inspector 추가
     - jsconsole 로그 추가
    """
    def __init__(self):
        super().__init__()
        _page = WebPagePlus()
        self.setPage(_page)
        self._setupInspector()

    def _setupInspector(self):
        """
        F12키를 누르면 "개발자 도구"가 노출됨
        """
        self.settings().setAttribute(QWebSettings.DeveloperExtrasEnabled, True)
        self.webInspector = QWebInspector(self)
        self.webInspector.setPage(self.page())

        shortcut = QShortcut(self)
        shortcut.setKey(Qt.Key_F12)
        shortcut.activated.connect(self._toggleInspector)
        self.webInspector.setVisible(False)


    def _toggleInspector(self):
        """
        F12키를 다시 누르면 "개발자 도구"가 사라짐
        """
        self.webInspector.setVisible(not self.webInspector.isVisible())



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


class KiwoomWebViewPlus(WebViewPlus):
    """
    키움 전용 Webview
    """
    def __init__(self):
        super().__init__()
        self._kiwoom = Kiwoom(self)
        self._mf = self.page().mainFrame()
        self._mf.addToJavaScriptWindowObject("kiwoom", self._kiwoom)
