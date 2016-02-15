angular
    .module('yapp')
    .factory('IpTablesService', function ($http) {

            var _hosts = [];

            var _getHosts = function () {

                return $http.get('http://iptables.local')
                    .then(function (response) {
                            _hosts = response.data;
                            return response.data
                        },
                        function (response) {
                            return false;
                        });
            }

            return {
                getHosts: _getHosts
            }
        }
    )
