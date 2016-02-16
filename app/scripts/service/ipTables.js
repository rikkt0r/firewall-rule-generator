angular
    .module('yapp')
    .factory('IpTablesService', function ($http, API_CONFIG) {

            var _hosts = [];
            var _rules = [];

            var _prepareUrl = function (endpoint) {
                return API_CONFIG.url + ':' + API_CONFIG.port + API_CONFIG['endpoints'][endpoint];
            }

            var _getHosts = function (forceReload) {

                forceReload = forceReload ? true : false;

                return $http.get(_prepareUrl('hosts'),{cache: forceReload})
                    .then(function (response) {
                            _hosts = response.data.hosts;
                            return _hosts;
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
                return $http.delete(_prepareUrl('hosts') + id + '/')
                    .then(function (response) {
                            return response.data
                        },
                        function () {
                            return false;
                        });
            };

            var _addHost = function (host) {
                return $http({
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

            var _editHost = function (id, _data){
                delete _data.id;
                _data.htype = _data.htype*1;
                for(var i = 0; i < _data.interfaces.length; i++){
                    _data.interfaces[i].netmask = _data.interfaces[i].netmask;
                }
                return $http({
                        'method': 'PUT',
                        'url': _prepareUrl('hosts') + id + '/',
                        'data': _data
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
                var url = _prepareUrl('available') + '/template/' + id;

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

                var url = _prepareUrl('available') + '/' + part;

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
                editHost: _editHost,
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
