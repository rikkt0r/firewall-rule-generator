'use strict';

/**
 * @ngdoc overview
 * @name yapp
 * @description
 * # yapp
 *
 * Main module of the application.
 */
angular
    .module('yapp', [
        'ui.router',
        'ngAnimate'
    ])
    .config(function ($stateProvider, $urlRouterProvider) {

        $urlRouterProvider.when('/dashboard', '/overview');
        //$urlRouterProvider.otherwise('/login');

        $stateProvider
            .state('base', {
                abstract: true,
                url: '',
                templateUrl: 'views/base.html'
            })
            // @TODO implement
            //.state('login', {
            //    url: '/login',
            //    parent: 'base',
            //    templateUrl: 'views/login.html',
            //    controller: 'LoginCtrl'
            //})
            .state('dashboard', {
                url: '',
                parent: 'base',
                templateUrl: 'views/dashboard.html',
                controller: 'DashboardCtrl'
            })
            .state('addnew', {
                url: '/addnew',
                parent: 'dashboard',
                templateUrl: 'views/entries/addnew.html',
                controller: 'AddNewCtrl'
            })
            .state('overview', {
                url: '/overview',
                parent: 'dashboard',
                templateUrl: 'views/dashboard/overview.html'
            })
            .state('reports', {
                url: '/reports',
                parent: 'dashboard',
                templateUrl: 'views/dashboard/reports.html'
            })
            .state('hosts', {
                url: '/hosts',
                abstract: true,
                parent: 'dashboard',
                template: '<ui-view/>',
                controller: 'HostsCtrl'
            })
            .state('hosts-index', {
                url: '/index',
                abstract: true,
                parent: 'hosts',
                templateUrl: 'views/hosts/list.html',
                controller: 'HostsCtrl'
            })
            .state('hosts-list', {
                url: '/list',
                parent: 'hosts',
                templateUrl: 'views/hosts/list.html',
                controller: 'HostsCtrl'
            })
            .state('hosts-graph', {
                url: '/graph',
                parent: 'hosts',
                templateUrl: 'views/hosts/graph.html',
                controller: 'HostsCtrl'
            });

    });