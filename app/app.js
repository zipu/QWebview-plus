/*global angular */

/**
 * The main KiwoomApi app module
 *
 * @type {angular.Module}
 */

var app = angular.module('kiwoomApp', ['ngRoute'])
	.config(function ($routeProvider) {
		'use strict';
        
		var routeConfig = {
			controller: 'TradingCtrl',
			templateUrl: 'views/tradingView.html'
		};

		$routeProvider
			.when('/', routeConfig)
			.otherwise({
				redirectTo: '/'
			});
	});
