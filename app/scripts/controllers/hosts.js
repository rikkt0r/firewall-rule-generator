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

    $scope.interfaces = [
        {
            'sys': 'eth0',
            'ip': '192.168.0.1',
            netmask: '255.255.255.0',
            desc: 'desc1'
        },
        {
            'sys': 'eth2',
            'ip': '192.168.0.2',
            netmask: '255.255.255.0',
            desc: 'desc2'
        },
        {
            'sys': 'eth3',
            'ip': '192.168.0.3',
            netmask: '255.255.255.0',
            desc: 'desc3'
        }
    ]

    $scope.tmpInterface = {
        'sys': 'eth3',
        'ip': '192.168.0.3',
        netmask: '255.255.255.0',
        desc: 'desc3'
    }

    $scope.submit = function () {
        $http({
            method: 'POST',
            url: 'localhost:5000/api/hosts'
        }).then(function successCallback(response) {
            $location.path('/hosts/list')
        }, function errorCallback(response) {
            $location.path('/hosts/list')
        });
    }

    $scope.removeInterface = function (idx) {
        $scope.host.interfaces.splice(idx, 1);
    }

    $scope.addInterface = function () {
        $scope.host.interfaces.push($scope.tmpInterface)
        $scope.tmpInterface = {
            'sys': '',
            'ip': '',
            netmask: '',
            desc: ''
        }
    }

});
