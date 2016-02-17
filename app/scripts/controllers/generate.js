'use strict';

/**
 * @ngdoc function
 * @name yapp.controller:MainCtrl
 * @description
 * # MainCtrl
 * Controller of yapp
 */
angular.module('yapp')
    .controller('GenerateCtrl', function ($scope, $state, $location, $stateParams, IpTablesService) {

        $scope.hosts = [];
        $scope.hostId = '';
        $scope.output = '';

        IpTablesService.getHosts(true)
            .then(function (data) {
                if (data.length)
                    $scope.hosts = data;
            });

        $scope.generate = function () {

            if(!$scope.hostId){
                return;
            }
            IpTablesService.generate($scope.hostId).then(
                function (response) {
                    console.log(response);
                    $scope.output = '';
                    var lines = response.lines;
                    for(var i = 0; i < lines.length; i++){
                        $scope.output += lines[i] + "\n";
                    }
                }
            )
        }

    });