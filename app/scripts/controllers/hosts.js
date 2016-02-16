'use strict';

/**
 * @ngdoc function
 * @name yapp.controller:MainCtrl
 * @description
 * # MainCtrl
 * Controller of yapp
 */
angular.module('yapp')
    .controller('HostsCtrl', function ($scope, $state, $location, $stateParams, IpTablesService) {

        $scope.$state = $state;

        IpTablesService.getHosts()
            .then(function (data) {
                $scope.hosts = data;
            });

        $scope.go = function ( path ) {
            $location.path( path );
        };

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

}).config(['$validationProvider', function ($validationProvider) {

        var expression = {
            required: function (value) {
                return !!value;
            },
            email: /^([\w-\.]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([\w-]+\.)+))([a-zA-Z]{2,4}|[0-9]{1,3})(\]?)$/,
            number: /^\d+$/,
            ip: /^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$/,
            minlength: function (value, scope, element, attrs, param) {
                return value.length >= param;
            },
            maxlength: function (value, scope, element, attrs, param) {
                return value.length <= param;
            }
        };

        var defaultMsg = {
            required: {
                error: 'This fild is mandatory'
            },
            number: {
                error: 'This should be Number'
            },
            ip: {
                error: 'This should be IPv4 address'
            },
            minlength: {
                error: 'This should be longer'
            },
            maxlength: {
                error: 'This should be shorter'
            }
        };
        $validationProvider.setExpression(expression).setDefaultMsg(defaultMsg);


        /**
         * Range Validation
         */
        $validationProvider
            .setExpression({
                range: function (value, scope, element, attrs) {
                    if (value >= parseInt(attrs.min) && value <= parseInt(attrs.max)) {
                        return value;
                    }
                }
            })
            .setDefaultMsg({
                range: {
                    error: 'Number should between 5 ~ 10',
                    success: 'good'
                }
            });
    }])
    .
    controller('HostAddCtrl', function ($scope, $http, $location, $state, $stateParams, IpTablesService) {

        $scope.host = {
            name: '',
            htype: '',
            interfaces: [],
            template: '',
            rules: ''
        };

        $scope.tmpInterface = {
            'sys': '1.1.1.1',
            'ip': '1.1.1.1',
            netmask: '2',
            desc: ''
        };

        var injector = angular.injector(['yapp']);
        var $validationProvider = injector.get('$validation');

        $scope.interfaceForm = {
            submit: function (form) {
                $validationProvider.validate(form)
                    .success(function () {
                        var obj = {
                            'sys': $scope.tmpInterface.sys,
                            'ip': $scope.tmpInterface.ip,
                            netmask: $scope.tmpInterface.netmask,
                            desc: $scope.tmpInterface.desc
                        };
                        $scope.host.interfaces.push(
                            obj
                        );
                        //$validationProvider.reset($scope.tmpInterface);
debugger;
                        //$scope.tmpInterface.sys = '';
                        //$scope.tmpInterface.ip = '';
                        //$scope.tmpInterface.netmask = '';
                        //$scope.tmpInterface.desc = '';

                    })
                    .error(function () {
                        console.log(2)
                    });
                //$validationProvider.reset($scope.tmpInterface);
            }

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
        };

        $scope.addInterface = function () {
            var obj = {
                'sys': $scope.tmpInterface.sys,
                'ip': $scope.tmpInterface.ip,
                netmask: $scope.tmpInterface.netmask,
                desc: $scope.tmpInterface.desc
            };
            $scope.host.interfaces.push(
                obj
            );

        }

    });
