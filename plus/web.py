# -*-coding: utf-8 -*-
import logging
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage, QWebEngineScript,QWebEngineSettings
from PyQt5.QtWidgets import QShortcut, QDialog, QGridLayout
from PyQt5.QtCore import Qt, QUrl, QFile, QIODevice

class WebViewPlus(QWebEngineView):
    """
	QWebEngineView 커스터마이징
	"""
    def __init__(self):
        super().__init__()
        self.setPage(WebPagePlus())
        self._loadQwebchannelJs()

        #F5 - Page reloading
        shortcut = QShortcut(self)
        shortcut.setKey(Qt.Key_F5)
        shortcut.activated.connect(self.reload)

    def debuggingMode(self, port):
        #Keyboard shortcuts
        shortcut = QShortcut(self)
        shortcut.setContext(Qt.ApplicationShortcut)
        shortcut.setKey(Qt.Key_F12)
        shortcut.activated.connect(self._toggleDevTool)

        self.devTool = QDialog(self)
        self.devTool.setWindowTitle("DevTool")
        self.devTool.setMinimumSize(680,480)
        self.devTool.resize(950, 800)
        self.devView = DevToolView(port)

        layout = QGridLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.devView)
        self.devTool.setLayout(layout)

    def _loadQwebchannelJs(self):
        # https://qt.gitorious.org/qt/qtwebchannel/source/?p=qt:qtwebchannel.git;a=blob;f=src/webchannel/qwebchannel.js;h=c270a95e6b63b62ccc07816ffa4824f45a427ba8;hb=HEAD
        qwebchannel_js = QFile('./js/qwebchannel.js')
        # qwebchannel_js = QFile(':/qtwebchannel/qwebchannel.js')
        if not qwebchannel_js.open(QIODevice.ReadOnly):
            raise SystemExit('Failed to load qwebchannel.js with error: %s' % qwebchannel_js.errorString())
        qwebchannel_js = bytes(qwebchannel_js.readAll()).decode('utf-8')

        qwebchannel_plus_js = QFile('./js/qwebchannel_plus.js')
        if not qwebchannel_plus_js.open(QIODevice.ReadOnly):
            raise SystemExit('Failed to load qwebchannel_plus.js with error: %s' % qwebchannel_plus_js.errorString())
        qwebchannel_plus_js = bytes(qwebchannel_plus_js.readAll()).decode('utf-8')

        script = QWebEngineScript()
        script.setSourceCode(qwebchannel_js)
        script.setName('qwebchannel')
        script.setWorldId(QWebEngineScript.MainWorld)
        script.setInjectionPoint(QWebEngineScript.DocumentCreation)
        script.setRunsOnSubFrames(True)

        script_plus = QWebEngineScript()
        script_plus.setSourceCode(qwebchannel_plus_js)
        script_plus.setName('qwebchannel_plus')
        script_plus.setWorldId(QWebEngineScript.MainWorld)
        script_plus.setInjectionPoint(QWebEngineScript.DocumentReady)
        script_plus.setRunsOnSubFrames(True)
        self.page().scripts().insert(script)
        self.page().scripts().insert(script_plus)


    def _toggleDevTool(self):
        """
        F12키를 다시 누르면 "개발자 도구"가 사라짐
        """
        if not self.devTool.isVisible():
            self.devView.removeDevTool()
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

    def javaScriptConsoleMessage(self, msg, lineNumber, sourceID):
        self.logger.warning("console(%s:%d): %s" % (sourceID, lineNumber, msg))


class DevToolView(QWebEngineView):
    """
    QWebEngineView 커스터마이징
    """
    def __init__(self, port):
        super().__init__()
        self.setPage(QWebEnginePage(self))
        self.load(QUrl("http://127.0.0.1:"+ port))

    def removeDevTool(self):
        # 리모트 디버그에서 자동으로 이동하는 스크립트
        loadScript = """
        var items = Array.prototype.slice.call(document.querySelectorAll(".item"));
        if (items.length) {
            document.body.style.opacity = "0.001";
            items = items.filter(v => {
                if(v.title === "QtWebEngine Remote Debugging") {
                    v.style.display = "none";
                    return false;
                } else {
                    return true;
                }
            });
            if(items.length === 1) {
                location.href = items[0].href;
            } else {
                document.body.style.opacity=1;
            }
        }
        """
        self.page().runJavaScript(loadScript)

