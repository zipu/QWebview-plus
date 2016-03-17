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

		self.ocx.connect(self.ocx, SIGNAL("OnEventConnect(int)"), self._OnEventConnect)
		self.ocx.connect(self.ocx, SIGNAL("OnReceiveTrData(QString, QString, QString, QString, QString, int, QString, QString, QString)"), self._OnReceiveTrData)
		self.ocx.connect(self.ocx, SIGNAL("OnReceiveMsg(QString, QString, QString, QString)"), self._OnReceiveMsg)
		self.ocx.connect(self.ocx, SIGNAL("OnReceiveRealData(QString, QString, QString)"), self._OnReceiveRealData)

	@pyqtSlot()
	def quit(self):
		self.commTerminate()
		QApplication.quit()

	# 통신 연결 상태 변경시 이벤트
	def _OnEventConnect(self, errCode):
		self.view.fireEvent("eventConnect.kiwoom", errCode)

	# 수신 메시지 이벤트
	def _OnReceiveMsg(self, scrNo, rQName, trCode, msg):
		self.view.fireEvent("receiveMsg.kiwoom", {
			"scrNo" : scrNo,
			"rQName" : rQName,
			"trCode": trCode,
			"msg" : msg
		})

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

	# 실시간 시세 이벤트
	def _OnReceiveRealData(self, jongmokCode, realType, realData):
		self.view.fireEvent("receiveRealData.kiwoom", {
			"jongmokCode" : jongmokCode,
			"realType" : realType,
			"realData": realData
		})

	# 로그인
	# 0 - 성공, 음수값은 실패
	@pyqtSlot(result=int)
	def commConnect(self):
		return self.ocx.dynamicCall("CommConnect()")

	# 로그인 상태 확인
	# 0:미연결, 1:연결완료, 그외는 에러
	@pyqtSlot(result=int)
	def getConnectState(self):
		return self.ocx.dynamicCall("GetConnectState()")

	# 로그 아웃
	@pyqtSlot()
	def commTerminate(self):
		self.ocx.dynamicCall("CommTerminate()")

	# 로그인한 사용자 정보를 반환한다.
	# “ACCOUNT_CNT” – 전체 계좌 개수를 반환한다.
	# "ACCNO" – 전체 계좌를 반환한다. 계좌별 구분은 ‘;’이다.
	# “USER_ID” - 사용자 ID를 반환한다.
	# “USER_NAME” – 사용자명을 반환한다.
	# “KEY_BSECGB” – 키보드보안 해지여부. 0:정상, 1:해지
	# “FIREW_SECGB” – 방화벽 설정 여부. 0:미설정, 1:설정, 2:해지
	@pyqtSlot(str,result=str)
	def getLoginInfo(self, tag):
		return self.ocx.dynamicCall("GetLoginInfo(QString)",[tag])


	# Tran 입력 값을 서버통신 전에 입력값일 저장한다.
	@pyqtSlot(str, str)
	def setInputValue(self, id, value):
		self.ocx.dynamicCall("SetInputValue(QString, QString)", id, value)

	# 통신 데이터를 송신한다.
	# 0이면 정상
	# OP_ERR_SISE_OVERFLOW – 과도한 시세조회로 인한 통신불가
	# OP_ERR_RQ_STRUCT_FAIL – 입력 구조체 생성 실패
	# OP_ERR_RQ_STRING_FAIL – 요청전문 작성 실패
	# OP_ERR_NONE – 정상처리
	@pyqtSlot(str, str, int, str, result=int)
	def commRqData(self, rQName, trCode, prevNext, screenNo):
		return self.ocx.dynamicCall("CommRqData(QString, QString, int, QString)", rQName, trCode, prevNext, screenNo)

	# 수신 받은 데이터의 반복 개수를 반환한다.
	@pyqtSlot(str, str, result=int)
	def getRepeatCnt(self, trCode, recordName):
		return self.ocx.dynamicCall("GetRepeatCnt(QString, QString)", trCode, recordName)

	# Tran 데이터, 실시간 데이터, 체결잔고 데이터를 반환한다.
# 1. Tran 데이터
# sJongmokCode : Tran명
# sRealType : 사용안함
# sFieldName : 레코드명
# nIndex : 반복인덱스
# sInnerFieldName: 아이템명
#
# 2. 실시간 데이터
# sJongmokCode : Key Code
# sRealType : Real Type
# sFieldName : Item Index
# nIndex : 사용안함
# sInnerFieldName:사용안함
#
# 3. 체결 데이터
# sJongmokCode : 체결구분
# sRealType : “-1”
# sFieldName : 사용안함
# nIndex : ItemIndex
# sInnerFieldName:사용안함
	@pyqtSlot(str, str, str, int, str, result=str)
	def commGetData(self, jongmokCode, realType, fieldName, index, innerFieldName):
		return self.ocx.dynamicCall("CommGetData(QString, QString, QString, int, QString)", jongmokCode, realType, fieldName, index, innerFieldName).strip()

	# 실시간데이터를 반환한다.
	@pyqtSlot(str, int, result=str)
	def getCommRealData(self, realType, fid):
		return self.ocx.dynamicCall("GetCommRealData(QString, int)",realType, fid)

	@pyqtSlot(str)
	def disconnectRealData(self, scnNo):
		self.ocx.dynamicCall("DisconnectRealData(QString)", scnNo)



	# 복수종목조회 Tran을 서버로 송신한다.
# OP_ERR_RQ_STRING – 요청 전문 작성 실패
# OP_ERR_NONE - 정상처리
#
# sArrCode – 종목간 구분은 ‘;’이다.
# nTypeFlag – 0:주식관심종목정보, 3:선물옵션관심종목정보
	@pyqtSlot(str, bool, int, int, str, str)
	def commKwRqData(self, arrCode, next, codeCount, typeFlag, rQName, screenNo):
		self.ocx.dynamicCall("CommKwRqData(QString, QBoolean, int, int, QString, QString)", arrCode, next, codeCount, typeFlag, rQName, screenNo)

	# 실시간 등록을 한다.
	@pyqtSlot(str, str, str, str)
	def setRealReg(self, screenNo, codeList, fidList, realType):
		self.ocx.dynamicCall("SetRealReg(QString, QString, QString, QString)", screenNo, codeList, fidList, realType)

	# 종목별 실시간 해제
	@pyqtSlot(str, str)
	def setRealRemove(self, scrNo, delCode):
		self.ocx.dynamicCall("SetRealRemove(QString, QString)", scrNo, delCode)