angular
  .module('kiwoomApp')
  .controller('TradingCtrl', TradingCtrl);

TradingCtrl.$inject = ['$scope'];

function TradingCtrl($scope) {
  'use strict';
   
   $scope.login_state = "로그인";
   
   $scope.login = function(){
       kiwoom.commConnect();
   }
     
  $scope.$on("eventConnect.kiwoom", function(event, errCode){
       alert('로그인 완료 :'+errCode);
       $scope.login_state = "로그아웃";
   });
}
