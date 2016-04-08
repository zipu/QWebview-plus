angular
  .module('kiwoomApp')
  .controller('TradingCtrl', TradingCtrl);

TradingCtrl.$inject = ['$scope'];

function TradingCtrl($scope) {

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
}
