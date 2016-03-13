#-*-coding: utf-8 -*-
from PyQt4.QtCore import SIGNAL, QObject, pyqtSlot
from PyQt4.QAxContainer import QAxWidget
from PyQt4.QtGui import QApplication
from plus.web import WebViewPlus

class KiwoomWebViewPlus(WebViewPlus):
    """
    키움 전용 Webview
    """
    def __init__(self):
        super().__init__()
        self._kiwoom = Kiwoom(self)
        self._mf = self.page().mainFrame()
        self._mf.addToJavaScriptWindowObject("kiwoom", self._kiwoom)

class Kiwoom(QObject):
	def __init__(self, view):
		super().__init__()
		self.view = view
		self.ocx = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")

		# 로그인 접속 여부 이벤트
		self.ocx.connect(self.ocx, SIGNAL("OnEventConnect(int)"), self._OnEventConnect)

		# receive data
		self.ocx.connect(self.ocx, SIGNAL("OnReceiveTrData(QString, QString, QString, QString, QString, int, QString, QString, QString)"), self._OnReceiveTrData)

	@pyqtSlot()
	def quit(self):
		QApplication.quit()

	# 통신 연결 상태 변경시 이벤트
	def _OnEventConnect(self, errCode):
		self.view.fireEvent("eventConnect.kiwoom", errCode)

	# Tran 수신시 이벤트
	def _OnReceiveTrData(self, scrNo, rQName , trCode, recordName, prevNext, dataLength, errorCode, message, splmMsg):
		self.view.fireEvent("receiveTrData.kiwoom", {
			"scrNo" : scrNo,
			"rQName" : rQName,
			"trCode": trCode,
			"recordName": recordName,
			"prevNext": prevNext,
			"dataLength": dataLength,
			"errorCode" : errorCode,
			"message" : message,
			"splmMsg" : splmMsg
		})

	@pyqtSlot()
	def commConnect(self):
		self.ocx.dynamicCall("CommConnect()")

	@pyqtSlot(str, str)
	def setInputValue(self, id, value):
		self.ocx.dynamicCall("SetInputValue(QString, QString)", id, value)

	# 통신 데이터를 송신한다.
	@pyqtSlot(str, str, int, str, result=int)
	def commRqData(self, rQName, trCode, prevNext, screenNo):
		return self.ocx.dynamicCall("CommRqData(QString, QString, int, QString)", rQName, trCode, prevNext, screenNo)

	# Tran 데이터, 실시간 데이터, 체결잔고 데이터를 반환한다.
	@pyqtSlot(str, str, str, int, str, result=str)
	def commGetData(self, jongmokCode, realType, fieldName, index, innerFieldName):
		return self.ocx.dynamicCall("CommGetData(QString, QString, QString, int, QString)", jongmokCode, realType, fieldName, index, innerFieldName).strip()
