angular.module('tradeSystem', ['ngRoute', 'ngMaterial'])
.config(['$routeProvider',
    function ($routeProvider) {
      $routeProvider
          .when('/', {
              templateUrl: 'view/static/tradingView.html',
              controller: 'TradingCtrl',
              controllerAs: 'trview'
          })
          .when('/stats', {
              templateUrl: 'view/static/stats.html'
          })
          .otherwise({
              redirectTo: '/'
          });
}]);
