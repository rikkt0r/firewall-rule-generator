angular
    .module('yapp')
    .factory('IpTablesService', function ($http, API_CONFIG) {

            var _hosts = [];
            var _rules = [];

            var _prepareUrl = function (endpoint) {
                return API_CONFIG.url + ':' + API_CONFIG.port + API_CONFIG['endpoints'][endpoint];
            }

            var _getHosts = function (forceReload) {

                if (_hosts.length && !forceReload) {
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
            };

            var _getRules = function (forceReload) {

                if (_rules.length && !forceReload) {
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
            };

            var _removeHost = function (id) {
                return $http.delete(_prepareUrl('hosts') + '/' + id)
                    .then(function (response) {
                            return response.data
                        },
                        function () {
                            return false;
                        });
            };

            var _addHost = function (host) {
                return $http.({
                        'method': 'POST',
                        'url': _prepareUrl('hosts'),
                        'data': host
                    })
                    .then(function (response) {
                        return response.data
                    },
                        function () {
                            return false;
                        });
            };

            var _getModules = function () {
                return _getAvailable('modules');

            };

            var _getTables = function () {
                return _getAvailable('tables');

            };

            var _getChains = function () {
                return _getAvailable('chains');

            };

            var _getTemplates = function () {
                return _getAvailable('templates');

            };

            var _getTemplate = function (id) {
                var url = _prepareUrl('available') + 'template/' + id;

                return $http.get(url)
                    .then(function (response) {
                            return response.data
                        },
                        function () {
                            return false;
                        });

            };

            var _getActions = function () {
                return _getAvailable('actions');

            };

            var _getAvailable = function (part) {

                if (['modules', 'chains', 'tables', 'actions', 'templates'].indexOf(part) < 0) {
                    throw "invalid option";
                }

                var url = _prepareUrl('available') + part;

                return $http.get(url)
                    .then(function (response) {
                            return response.data
                        },
                        function () {
                            return false;
                        });
            };

            return {
                getHosts: _getHosts,
                addHost: _addHost,
                removeHost: _removeHost,
                getRules: _getRules,
                getAvailable: _getAvailable,
                getModules: _getModules,
                getTables: _getTables,
                getChains: _getChains,
                getTemplates: _getTemplates,
                getActions: _getActions,
                getTemplate: _getTemplate
            }
        }
    )
