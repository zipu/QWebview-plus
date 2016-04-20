angular.module('kiwoomApp')
  .factory('Kiwoom', ['$filter',function ($filter) {
      
      var login = function(){
         kiwoom.getConnectState()? kiwoom.commTerminate() : kiwoom.commConnect();        
      };
         
      var getLoginInfo = function(){
          return {
             account : kiwoom.getLoginInfo('ACCNO').replace(/;$/,'').split(';'),
             user : {
                 id : kiwoom.getLoginInfo('USER_ID'),
                 name : kiwoom.getLoginInfo('USER_NAME')
             }
          };
      };    
          
      var chart = function(code){
          kiwoom.setInputValue('종목코드', code);
          kiwoom.setInputValue('기준일자', $filter('date')(new Date(), 'yyyyMMdd'));
          kiwoom.setInputValue('수정주가구분 ', 0);
          // rQName과 화면번호는 사용자가 지정하여 구분하는 값
          kiwoom.commRqData('주식일봉차트조회요청', 'opt10081', 0, '0002');
      };
      
      var search = function(code){
          kiwoom.setInputValue('종목코드', code);
          // rQName과 화면번호는 사용자가 지정하여 구분하는 값
          kiwoom.commRqData('주식기본정보', 'opt10001', 2, '0001');
 
      };
      
      
      var response = function(e, data){
          console.info('< '+e.name+' > received from the server...');
          console.info('Data info :', data);
          
          switch (e.name){
             case 'eventConnect.kiwoom':
                console.info(kiwoom.parseErrorCode(data));
             //   console.log(kiwoom.getLoginInfo('ACCNO').replace(/;$/,'').split(';'));
                break;
              
             case 'receiveMsg.kiwoom':
                console.info({
                    'scrNo' : data.scrNo,
                    'rQName' : data.rQName,
                    'trCode': data.trCode,
                    'msg' : data.msg
                });
                break;
                
             case 'receiveTrData.kiwoom':
                var len = kiwoom.getRepeatCnt(data.trCode, data.rQName);
                console.info('rQName : '+data.rQName+', trCode: '+data.trCode+', repeadCnt : '+len);
              
                switch(data.trCode) {
                  case 'opt10001' :
                      for(var i=0; i<len; i++) {
                          console.log('TR 데이터',{
                              // "종목명" : kiwoom.commGetData(data.trCode, "", data.rQName, i, "종목명"),
                              // "시가총액" : kiwoom.commGetData(data.trCode, "", data.rQName, i, "시가총액"),
                              // "거래량" : kiwoom.commGetData(data.trCode, "", data.rQName, i, "거래량"),
                              // "현재가" : kiwoom.commGetData(data.trCode, "", data.rQName, i, "현재가")
                              '종목명' : kiwoom.plusGetTrData(data.trCode, data.rQName, i, '종목명'),
                              '시가총액' : kiwoom.plusGetTrData(data.trCode, data.rQName, i, '시가총액'),
                              '거래량' : kiwoom.plusGetTrData(data.trCode, data.rQName, i, '거래량'),
                              '현재가' : kiwoom.plusGetTrData(data.trCode, data.rQName, i, '현재가')
                          });
                      }
                      break;
                  case 'opt10081' :
                      console.log('TR 데이터', JSON.parse(kiwoom.getCommDataEx(data.trCode, data.rQName)));
                      break;
                }
                break;
                
              case 'receiveRealData':
                 console.info('실시간데이터', {
                     'jongmokCode' : data.jongmokCode,
                     'realType' : data.realType,
                     'realData': data.realData
                 });
                 console.log(kiwoom.plusGetRealData(data.jongmokCode, data.realType, 10));
                 break;
          }
      };
      
      var EVENTS = [
          'eventConnect.kiwoom',
          'receiveMsg.kiwoom',
          'receiveTrData.kiwoom',
          'receiveRealData.kiwoom',
          'receiveChejanData.kiwoom',
          'receiveConditionVer.kiwoom',
          'receiveTrCondition.kiwoom',
          'receiveRealCondition.kiwoom'
      ];
      
      return {
          login : login,
          getLoginInfo : getLoginInfo,
          chart : chart,
          search : search,
          respondTo : response,
          EVENTS : EVENTS
      };
  }]);
 
