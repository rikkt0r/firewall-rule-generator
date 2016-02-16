'use strict';

/**
 * @ngdoc function
 * @name yapp.controller:MainCtrl
 * @description
 * # MainCtrl
 * Controller of yapp
 */
angular.module('yapp')
  .controller('DashboardCtrl', function($scope, $state, IpTablesService) {

    $scope.$state = $state;
      IpTablesService.getHosts()
          .then(function (data) {
              $scope.hosts = data;
          });
  });
