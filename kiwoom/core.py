#-*-coding: utf-8 -*-
from PyQt4.QtCore import *
from PyQt4.QAxContainer import *
from PyQt4.QtGui import QApplication
from plus import WebViewPlus

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
	# http://stackoverflow.com/questions/2490825/how-to-trigger-event-in-javascript
	customEvent = """
	var event = document.createEvent("CustomEvent");
	event.initCustomEvent("{type}", true, true, {detail} );
	document.dispatchEvent(event);
	"""

	def __init__(self, view):
		super().__init__()
		self.view = view
		self.ocx = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")

		# 로그인 접속 여부 이벤트
		self.ocx.connect(self.ocx, SIGNAL("OnEventConnect(int)"), self._OnEventConnect)

		# receive data
		self.ocx.connect(self.ocx, SIGNAL("OnReceiveTrData(QString, QString, QString, QString, QString, int, QString, QString, QString)"), self._OnReceiveTrData)


	def fireEvent(self, type, detail):
		self.view.page().mainFrame().evaluateJavaScript(Kiwoom.customEvent.format(type=type, detail=detail))

	@pyqtSlot()
	def quit(self):
		QApplication.quit()

	# 통신 연결 상태 변경시 이벤트
	def _OnEventConnect(self, errCode):
		self.fireEvent("kiwoom:connect", errCode)

	# Tran 수신시 이벤트
	def _OnReceiveTrData(self, scrNo, rQName , trCode, recordName, prevNext, dataLength, errorCode, message, splmMsg):
		if rQName == "Request1":
			name = self.ocx.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trCode, "", rQName, 0, "종목명")
			volume = self.ocx.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trCode, "", rQName, 0, "거래량")
			print(name,volume)
			print("같은거", self.commGetData(trCode, "", rQName, 0, "종목명"))
			self.fireEvent("kiwoom:receiveTR", {
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
	def setInputValue(self, key, value):
		self.ocx.dynamicCall("SetInputValue(QString, QString)", key, value)

	# 통신 데이터를 송신한다.
	@pyqtSlot(str, str, int, str, result=int)
	def commRqData(self, name, trCode, prevNext, screenNo):
		return self.ocx.dynamicCall("CommRqData(QString, QString, int, QString)",name, trCode, prevNext, screenNo)

	# Tran 데이터, 실시간 데이터, 체결잔고 데이터를 반환한다.
	@pyqtSlot(str, str, str, int, str, result=str)
	def commGetData(self, trCode, realType, fieldName, index, innerFieldName):
		print("js", trCode, realType, fieldName, index, innerFieldName)
		return self.ocx.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trCode, realType, fieldName, index, innerFieldName)
