angular
    .module('yapp')
    .factory('IpTablesService', function ($http, API_CONFIG) {

            var _hosts = [];
            var _rules = [];

            var _prepareUrl = function(endpoint){
                return API_CONFIG.url + ':' + API_CONFIG.port + API_CONFIG['endpoints'][endpoint];
            }

            var _getHosts = function (forceReload) {

                if(_hosts.length && !forceReload){
                    return _hosts;
                }

                return $http.get(_prepareUrl('hosts'))
                    .then(function (response) {
                            _hosts = response.data;
                            return response.data
                        },
                        function () {
                            return false;
                        });
            }

            var _getRules = function (forceReload) {

                if(_rules.length && !forceReload){
                    return _rules;
                }

                return $http.get(_prepareUrl('rules'))
                    .then(function (response) {
                            _rules = response.data;
                            return response.data
                        },
                        function () {
                            return false;
                        });
            }

            return {
                getHosts: _getHosts,
                getRules: _getRules,
            }
        }
    )
