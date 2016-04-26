angular.module('tradeSystem')
  .factory('KiwoomService', ['$filter',function ($filter) {
      
      new QWebChannel(qt.webChannelTransport, function(channel){
          kiwoom = channel.objects.kiwoom;
          kiwoom.fireEvent.connect(function(event, data){
              console.info('< '+event+' > received from the server...');
              console.info('Data info :'+JSON.parse(data));
              respondTo(event,data);
          });
      });
      
      var login = function(){
        kiwoom.getConnectState(function(state){
             if (state ==1){
                 kiwoom.commTerminate();
             } else if (state == 0){
                 kiwoom.commConnect(function(){
                      kiwoom.loginEvent.connect(function(event,data){
                          if (data == 0){
                             console.log("로그인 성공");
                             //alert(kiwoom.getLoginInfo('ACCNO').replace(/;$/,'').split(';'));
                          } else if (data < 0) 
                             console.log("로그인 실패");
                      });
                 });
             }
        });
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
      
      var ConnectState = function(callback){
          kiwoom.getConnectState(function(state){
              callback(state);
          });
      };
      
      var respondTo = function(e, data){

          switch (e.name){
             
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
                
              case 'receiveRealData.kiwoom':
                 console.info('실시간데이터', {
                     'jongmokCode' : data.jongmokCode,
                     'realType' : data.realType,
                     'realData': data.realData
                 });
                 console.log(kiwoom.plusGetRealData(data.jongmokCode, data.realType, 10));
                 break;
          }
      };
      
      return {
          login : login,
          getLoginInfo : getLoginInfo,
          chart : chart,
          search : search,
          ConnectState : ConnectState
      };
  }]);
 
