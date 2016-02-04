'use strict';

/**
 * @ngdoc function
 * @name yapp.controller:MainCtrl
 * @description
 * # MainCtrl
 * Controller of yapp
 */
angular.module('yapp')
    .controller('HostsCtrl', function ($scope, $state) {

        $scope.$state = $state;
        $scope.hosts = {
            "a" : 123
        };

    });
