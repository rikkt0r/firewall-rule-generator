'use strict';

/**
 * @ngdoc function
 * @name yapp.controller:MainCtrl
 * @description
 * # MainCtrl
 * Controller of yapp
 */
angular.module('yapp')
    .controller('HostsCtrl', function ($scope, $state, $stateParams, IpTablesService) {

        $scope.$state = $state;

        IpTablesService.getHosts()
            .then(function (data) {
                $scope.hosts = data;
            });

    }).controller('HostShowCtrl', function ($scope, $state, $stateParams, IpTablesService) {


    $scope.$state = $state;
    var id = $stateParams.id;
    IpTablesService.getHosts()
        .then(function (data) {
            $scope.hosts = data;
            for (var i = 0, len = data.length; i < len; i++) {
                if (id == data[i].id) {
                    $scope.host = data[i];
                    break;
                }
            }
        });

}).
controller('HostAddCtrl', function ($scope, $http, $location, $state, $stateParams, IpTablesService) {

    $scope.host = {
        name: '',
        htype: '',
        interfaces: [],
        template: '',
        rules: ''
    };

    $scope.tmpInterface = {
        'sys': '',
        'ip': '',
        netmask: '',
        desc: ''
    }

    $scope.submit = function () {

        $http({
            method: 'POST',
            url: 'localhost:5000/api/hosts'
        }).then(function successCallback(response) {
            //$location.path('/hosts/list')
        }, function errorCallback(response) {
            //$location.path('/hosts/list')
        });
    }

    $scope.removeInterface = function (idx) {
        $scope.host.interfaces.splice(idx, 1);
    }

    $scope.addInterface = function () {
        debugger;
        $scope.host.interfaces.push($scope.tmpInterface)
        $scope.tmpInterface = {
            'sys': '',
            'ip': '',
            netmask: '',
            desc: ''
        }
    }

});
