angular
  .module('kiwoomApp')
  .controller('TradingCtrl', TradingCtrl);

TradingCtrl.$inject = ['$scope', '$interval', '$timeout','Kiwoom'];

function TradingCtrl($scope, $interval,$timeout, Kiwoom) {

    var trview = this;

    trview.code = '214450';

    trview.login = function(){
        trview.isDisabled = true;
        $timeout(function(){
            Kiwoom.login();
        },0).finally(function(){
            trview.isDisabled = false;
        });
    };
    
    trview.search = function(){
        return Kiwoom.search(trview.code);
    };
    
    trview.chart = function(){
        return Kiwoom.chart(trview.code);
    };
    
    //시그널
    Kiwoom.EVENTS.forEach(function(event){
        $scope.$on(event, Kiwoom.respondTo);
    });
     
       
    //연결상태 정보
    $interval(function(){
        var state = kiwoom.getConnectState();
        if (state == 1){
            trview.connection = '연결중';
            trview.loginstate = '로그아웃';
        } else {
            trview.connection = '미연결 상태';
            trview.loginstate = '로그인';
        }
    }, 3000);
}