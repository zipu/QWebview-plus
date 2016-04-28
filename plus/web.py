# -*-coding: utf-8 -*-
import logging
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage, QWebEngineScript
from PyQt5.QtWidgets import QShortcut
from PyQt5.QtCore import Qt, QFile, QIODevice

class WebViewPlus(QWebEngineView):
    """
	WebView 커스터마이징
	 - jsconsole 로그 추가
	 - webview에서 document로 이벤트를 발생함.
	"""
    def __init__(self):
        super().__init__()
        self.setPage(WebPagePlus())
        self._loadQwebchannelJs()
        self._initShortcut()

    def _loadQwebchannelJs(self):
        # https://qt.gitorious.org/qt/qtwebchannel/source/?p=qt:qtwebchannel.git;a=blob;f=src/webchannel/qwebchannel.js;h=c270a95e6b63b62ccc07816ffa4824f45a427ba8;hb=HEAD
        qwebchannel_js = QFile('./js/qwebchannel.js')
        # qwebchannel_js = QFile(':/qtwebchannel/qwebchannel.js')
        if not qwebchannel_js.open(QIODevice.ReadOnly):
            raise SystemExit('Failed to load qwebchannel.js with error: %s' % qwebchannel_js.errorString())
        qwebchannel_js = bytes(qwebchannel_js.readAll()).decode('utf-8')

        script = QWebEngineScript()
        script.setSourceCode(qwebchannel_js)
        script.setName('qwebchannel')
        script.setWorldId(QWebEngineScript.MainWorld)
        script.setInjectionPoint(QWebEngineScript.DocumentCreation)
        script.setRunsOnSubFrames(True)
        self.page().scripts().insert(script)

    def _initShortcut(self):
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

    def javaScriptConsoleMessage(self, msg, lineNumber, sourceID):
        self.logger.warning("console(%s:%d): %s" % (sourceID, lineNumber, msg))
