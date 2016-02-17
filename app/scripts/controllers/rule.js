'use strict';

/**
 * @ngdoc function
 * @name yapp.controller:MainCtrl
 * @description
 * # MainCtrl
 * Controller of yapp
 */
angular.module('yapp')
    .controller('HostRuleCtrl', function ($scope, $state, $location, $stateParams, IpTablesService) {

        $scope.host = {};
        $scope.chains = [];
        $scope.tables = [];
        $scope.actions = [];
        $scope.loglevels = [];
        $scope.modules = [{
            "sys": "tcp",
            "desc": "TCP, enabled automatically when -p tcp",
            "params": [
                {"sys": "sport", "desc": "source port:  port or port:port"},
                {"sys": "dport", "desc": "destination port:  port or port:port"},
                {
                    "sys": "tcp-flags",
                    "desc": "flags for tcp. which flags to examined <space> which should be set (ALL=SYN,ACK,FIN,RST,URG,PSH)  example: SYN,ACK FIN"
                },
            ]
        },
            {
                "sys": "udp",
                "desc": "UDP, enabled automatically when -p udp",
                "params": [
                    {"sys": "sport", "desc": "source port:  port or port:port"},
                    {"sys": "dport", "desc": "destination port:  port or port:port"},
                ]
            },
            {
                "sys": "icmp",
                "desc": "ICMP, enabled automatically when -p icmp",
                "params": [
                    {"sys": "icmp-type", "desc": "type of icmp, string or number, ex: echo-request or 8"},
                ]
            }];

        $scope.mode = 'advanced';

        $scope.addModuleName = '';
        $scope.addModuleParams = [];
        $scope.addModule = function(){
            var module = {
                sys: $scope.addModuleName,
                params: []
            };

            for (var key in $scope.addModuleParams) {
                // skip loop if the property is from prototype
                if (!$scope.addModuleParams.hasOwnProperty(key)) continue;

                var obj = $scope.addModuleParams[key];

                for (var prop in obj) {
                    // skip loop if the property is from prototype
                    if (!obj.hasOwnProperty(prop)) continue;

                    var param = {
                        sys: key,
                        value: obj[prop]
                    };
                }
                module.params.push(param);
            }

            $scope.rule.modules.push(module);
            $scope.addModuleName = '';
            $scope.addModuleParams = [];
        };

        $scope.removeModule = function(idx){
            $scope.rule.modules.splice(idx, 1);
        }

        $scope.rule = {
            "table": "filter",
            "chain": "",
            "protocol": "",
            'interface': '',
            "modules": [
                {
                    "sys": "state", "params": [
                    {"sys": "state", "value": "RELATED,ESTABLISHED"},
                ]
                },{
                    "sys": "sta2te", "params": [
                    {"sys": "state", "value": "RELATED,ESTABLISHED"},
                ]
                }
            ],
            "action": "",
            "params": []
        };

        /**
         * prepare and send rule
         */
        $scope.submit = function () {
            var rulePrepared = prepareRule();
            IpTablesService.addRule($scope.host.id, rulePrepared).then(
                function(response){
                    console.log(response)
                }
            )
        }

        var prepareRule = function() {
            var rulePrepared = {};
            rulePrepared.table = $scope.rule.table;
            rulePrepared.chain = $scope.rule.chain;
            rulePrepared.protocol = $scope.rule.protocol;
            rulePrepared.protocol_reverse = $scope.rule.protocol_reverse;
            rulePrepared.source = $scope.rule.source;
            rulePrepared.source_mask = $scope.rule.source_mask*1;
            rulePrepared.source_reverse = $scope.rule.source_reverse;
            rulePrepared.destination = $scope.rule.destination;
            rulePrepared.destination_mask = $scope.rule.destination_mask*1;
            rulePrepared.destination_reverse = $scope.rule.destination_reverse;
            rulePrepared.action = $scope.rule.action;
            rulePrepared.modules = [];

            if ($scope.rule.protocol !== '') {
                rulePrepared.modules.push({
                    sys: $scope.rule.protocol,
                    params: []
                });
            }

            for (var i = 0; i < rulePrepared.modules.length; i++) {
                for (var key in $scope.rule.params) {
                    // skip loop if the property is from prototype
                    if (!$scope.rule.params.hasOwnProperty(key)) continue;

                    var obj = $scope.rule.params[key];

                    var params = [];
                    for (var prop in obj) {
                        // skip loop if the property is from prototype
                        if (!obj.hasOwnProperty(prop)) continue;

                        params.push({
                            sys: prop,
                            value: obj[prop].value
                        })
                    }
                    rulePrepared.modules[i].params = params;
                }
            }

            rulePrepared.table = $scope.rule.table;
            return rulePrepared;
        }

        $scope.getModuleParams = function (module) {
            if (!module) {
                return [];
            }

            for (var i = 0; i < $scope.modules.length; i++) {
                if (module == $scope.modules[i].sys) {
                    return $scope.modules[i].params;
                }
            }
            return [];
        };

        $scope.getChains = function (advanced) {
            advanced = advanced ? true : false;

            if (advanced) {
                return $scope.chains;
            }

            var result = [];
            for (var i = 0; i < $scope.chains.length; i++) {
                if ($scope.chains[i].advanced !== true) {
                    result.push($scope.chains[i]);
                }
            }
            return result;

        };

        $scope.getActions = function (advanced) {
            advanced = advanced ? true : false;

            if (advanced) {
                return $scope.actions;
            }

            var result = [];
            for (var i = 0; i < $scope.actions.length; i++) {
                if ($scope.actions[i].advanced !== true) {
                    result.push($scope.actions[i]);
                }
            }
            return result;

        };

        $scope.setAdvancedMode = function () {
            $scope.mode = 'advanced';
        }

        $scope.setBasicMode = function () {
            $scope.mode = 'basic';
        }


        var id = $stateParams.id;
        IpTablesService.getHosts(false)
            .then(function (data) {
                $scope.hosts = data;
                for (var i = 0, len = data.length; i < len; i++) {
                    if (id == data[i].id) {
                        $scope.host = data[i];
                        break;
                    }
                }
            });

        IpTablesService.getChains()
            .then(function (data) {
                $scope.chains = data;
            });

        IpTablesService.getTables()
            .then(function (data) {
                $scope.tables = data;
            });

        IpTablesService.getActions()
            .then(function (data) {
                $scope.actions = data;
            });


        IpTablesService.getLogLevels()
            .then(function (data) {
                $scope.loglevels = data;
            });

        IpTablesService.getModules()
            .then(function (data) {
                if (data.length)
                    $scope.modules = data;
            });

    });