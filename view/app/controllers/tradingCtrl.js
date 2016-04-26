angular
  .module('tradeSystem')
  .controller('TradingCtrl', TradingCtrl);

TradingCtrl.$inject = ['$scope', '$interval', '$timeout','KiwoomService'];

function TradingCtrl($scope, $interval,$timeout, KiwoomService) {

    var trview = this;
    trview.code = '003000';

    trview.login = function(){
        KiwoomService.login();
    };
    
    trview.search = function(){
        return KiwoomService.search(trview.code);
    };
    
    trview.chart = function(){
        return KiwoomService.chart(trview.code);
    };
       
    //연결상태 정보
    $interval(function(){
        KiwoomService.ConnectState(function(state){
            if (state == 1){
                trview.connection = '연결중';
                trview.loginstate = '로그아웃';
            } else {
                trview.connection = '미연결 상태';
                trview.loginstate = '로그인';
            }
        });
    }, 3000);
}