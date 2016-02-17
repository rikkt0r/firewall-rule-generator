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

        $scope.go = function (path) {
            $location.path(path);
        };

    }).controller('HostShowCtrl', function ($scope, $state, $location, $stateParams, IpTablesService) {

    $scope.$state = $state;


    var id = $stateParams.id;
    $scope.rules = [];

    IpTablesService.getHosts(false)
        .then(function (data) {
            $scope.hosts = data;
            for (var i = 0, len = data.length; i < len; i++) {
                if (id == data[i].id) {
                    $scope.host = data[i];

                    //get rules
                    IpTablesService.getRules($scope.host.id)
                        .then(function(response){
                            $scope.rules = response.rules;
                        })

                    break;
                }
            }
        });

    $scope.rules = [];

    $scope.oldHost = {};
    $scope.editMode = false;
    $scope.toggleEdit = function () {
        if ($scope.editMode === false) {
            //$scope.oldHost =
            angular.copy($scope.host, $scope.oldHost);
        }
        $scope.editMode = !$scope.editMode;
    }
    $scope.cancelEdit = function () {
        angular.copy($scope.oldHost, $scope.host);
        $scope.oldHost = {};
        $scope.editMode = false;
    }

    $scope.save = function () {
        IpTablesService.editHost($scope.host.id,$scope.host);
        $state.go($state.current, {}, {reload: true});
    }

    $scope.htypeOptions = [
        {id: 1, value: 'PC/Laptop'},
        {id: 2, value: 'Server'},
        {id: 3, value: 'Firewall'},
        {id: 4, value: 'Other'}
    ]

    $scope.getHostType = function (val) {
        switch(val){
            case 1: return 'PC/Laptop';
            case 2: return 'Server';
            case 3: return 'Firewall';
            default: return 'Other';
        }
    }
    $scope.htypeSelected = function (val) {
        return val == host.htype;
    }
    $scope.removeInterface = function (idx) {
        $scope.host.interfaces.splice(idx, 1);
    };

    $scope.removeRule = function (ruleId) {
        IpTablesService.removeRule($scope.host.id, ruleId).then(
            function(){
                $state.go($state.current, {}, {reload: true});
            }
        )
    };

    $scope.newInterface = {
        ip : '',
        sys: '',
        netmask: 0,
        desc: ''
    };

    $scope.addInterface = function(){
        if(
            !($scope.newInterface.ip
            && $scope.newInterface.netmask
            && $scope.newInterface.sys)
        ){
            return false;
        }
        var newInterfaceTmp = {};
        angular.copy($scope.newInterface, newInterfaceTmp);
        $scope.newInterface = {
            ip : '',
            sys: '',
            netmask: 0,
            desc: ''
        };

        newInterfaceTmp.netmask = newInterfaceTmp.netmask*1;

        $scope.host.interfaces.push(newInterfaceTmp);
    }

    $scope.interfaceValid = function(){
        return (($scope.host.interface.ip)
        && ($scope.host.interface.netmask)
        && ($scope.host.interface.sys));
    }

    $scope.addRule = function(){
        $location.path('/hosts/rule/'+$scope.host.id);
    }

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

        IpTablesService.getTemplates().then(
            function (data) {
                $scope.templates = data;
            }
        )
        //$scope.templates = [
        //    {"id": "bc06c2e6-ccb9-481b-9363-2e20b0a46258", "name": "All-negation", "desc": "All packets on input/output dropped by default"},
        //    {"id": "5837272e-80cc-4534-a10b-fb4ace090813", "name": "All-ok", "desc": "All packets on input/output accepted by default"},
        //];

        var injector = angular.injector(['yapp']);
        var $validationProvider = injector.get('$validation');

        $scope.interface = {
            checkValid: $validationProvider.checkValid,
            submit: function (form) {
                //$validationProvider.validate(form)
                //    .success(
                //        function(){
                //            console.log('success');
                //        }
                //    )
                //    .error(
                //        function(){
                //            console.log('error');
                //        }
                //    );

                $scope.addInterface();
            },
            reset: function (form) {
            }
        };

        $scope.submit = function () {
            $scope.host.htype = $scope.host.htype * 1;
            IpTablesService.addHost($scope.host).then(function(data){
                $location.path('/hosts/'+data.id);
            })

        }

        $scope.removeInterface = function (idx) {
            $scope.host.interfaces.splice(idx, 1);
        };

        $scope.interfaceValid = function(){
            return (($scope.interface.ip)
            && ($scope.interface.netmask)
            && ($scope.interface.sys));
        }

        $scope.addInterface = function () {
            var obj = {
                'sys': $scope.interface.sys,
                'ip': $scope.interface.ip,
                netmask: $scope.interface.netmask * 1,
                desc: $scope.interface.desc
            };
            $scope.host.interfaces.push(
                obj
            );

        }

    });
