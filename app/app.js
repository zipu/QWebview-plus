angular.module('kiwoomApp', ['ngRoute'])
	.config(function ($routeProvider) {
        
		var routeConfig = {
			templateUrl: 'views/tradingView.html',
            controller: 'TradingCtrl',
            controllerAs: 'trview'
		};

		$routeProvider
			.when('/', routeConfig)
			.otherwise({
				redirectTo: '/'
			});
	});
