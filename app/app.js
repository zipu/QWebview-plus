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
    
    

/* 
     var kiwoomAPP = angular.module("kiwoomApp", ['ngRoute'])
     
     .config(function($routeProvider){
         $routeProvider.when("/",
            {
                templateUrl : "app.html",
                controller: "apiController",
                controllAs: "api"
            });
         });
     
     kiwoomAPP.controller('apiController',function($scope){
         $scope.login = function(){
             kiwoom.commConnect();
         }
     });
 */