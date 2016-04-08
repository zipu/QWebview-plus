angular
  .module('kiwoomApp')
  .controller('TradingCtrl', TradingCtrl);

TradingCtrl.$inject = ['$scope'];

function TradingCtrl($scope) {
<<<<<<< HEAD

  $scope.login_state = "Login"
  $scope.message = "show message here"
  
  $scope.login = function(){
      kiwoom.commConnect();
  }
  
  $scope.$on("eventConnect.kiwoom", function(event, errCode){
       if (errCode == 0){
           $scope.message = "로그인 성공 (code: "+errCode+" )";
           $scope.login_state = "Logout"
           
       } else {
           $scope.message = "로그인 실패 (code: "+errCode+" )";
       }  
 });
=======
  'use strict';
   
   $scope.login_state = "로그인";
   
   $scope.login = function(){
       kiwoom.commConnect();
   }
     
  $scope.$on("eventConnect.kiwoom", function(event, errCode){
       alert('로그인 완료 :'+errCode);
       $scope.login_state = "로그아웃";
   });
>>>>>>> 35ff049b79c20dadf021439b2c3d579051ae8a45
}
