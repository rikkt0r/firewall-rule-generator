angular
    .module('yapp')
    .directive('networkGraph', networkGraph);

/** @ngInject */
function networkGraph() {
    var directive = {
        restrict: 'E',
        templateUrl: 'scripts/directives/networkGraph/network-graph.html',
        scope: {
            hosts: '='
        },
        controller: networkGraphCtrl,
        controllerAs: 'vm',
    };


    return directive;
}

/** @ngInject */
function networkGraphCtrl($scope) {

    var nodes = [];
    var edges = [];
    var network = null;

    var DIR = '../../images/';
    var EDGE_LENGTH_MAIN = 150;
    var EDGE_LENGTH_SUB = 50;

    //var tmpHosts = [
    //    {
    //        id: 1,
    //        ip: {
    //            address: '192.168.0.1',
    //            mask: '255.255.255.0',
    //            network: '192.168.0.1'
    //        },
    //        name: 'host 1'
    //    }, {
    //        id: 2,
    //        ip: {
    //            address: '192.168.0.2',
    //            mask: '255.255.255.0',
    //            network: '192.168.0.1'
    //        },
    //        name: 'host 2'
    //    }, {
    //        id: 3,
    //        ip: {
    //            address: '192.168.0.3',
    //            mask: '255.255.255.0',
    //            network: '192.168.0.1'
    //        },
    //        name: 'host 3'
    //    },
    //];
    //$scope.hosts = localStorage.setItem('hosts', JSON.stringify(tmpHosts));
    //
    //try {
    //    $scope.hosts = JSON.parse(localStorage.getItem('hosts'));
    //} catch (e) {
    //    $scope.hosts = {};
    //}

    var getNodes = function (hosts) {

        if(!Array.isArray(hosts)){return []}

        var nodes = [];

        function addToNodes(element) {
            var node = {
                id: element.id,
                label: element.name,
                image: DIR + 'host1.png', shape: 'image'
            }
            nodes.push(node);
        }

        hosts.forEach(addToNodes);

        return nodes;

        return [
            {id: 1, label: 'Main', image: DIR + 'router1.png', shape: 'image'},
            {id: 2, label: 'Office', image: DIR + 'router1.png', shape: 'image'},
            {id: 3, label: 'Wireless', image: DIR + 'router1.png', shape: 'image'},
            {id: 104, label: 'Internet', image: DIR + 'host1.png', shape: 'image'},
            {id: 101, label: 'Printer', image: DIR + 'host1.png', shape: 'image'},
            {id: 102, label: 'Laptop', image: DIR + 'host1.png', shape: 'image'},
            {id: 103, label: 'network drive', image: DIR + 'host1.png', shape: 'image'}
        ]
    };

    nodes = getNodes($scope.hosts);

    //edges.push({from: 1, to: 2, length: EDGE_LENGTH_MAIN});
    //edges.push({from: 1, to: 3, length: EDGE_LENGTH_MAIN});
    //
    //for (var i = 4; i <= 7; i++) {
    //    //nodes.push({id: i, label: 'Computer', image: DIR + 'host1.png', shape: 'image'});
    //    //edges.push({from: 2, to: i, length: EDGE_LENGTH_SUB});
    //}
    //
    //edges.push({from: 2, to: 101, length: EDGE_LENGTH_SUB});
    //edges.push({from: 3, to: 102, length: EDGE_LENGTH_SUB});
    //edges.push({from: 1, to: 103, length: EDGE_LENGTH_SUB});
    //edges.push({from: 1, to: 104, length: EDGE_LENGTH_SUB});
    //
    //for (var i = 200; i <= 201; i++) {
    //    nodes.push({id: i, label: 'Smartphone', image: DIR + 'host1.png', shape: 'image'});
    //    edges.push({from: 3, to: i, length: EDGE_LENGTH_SUB});
    //}

    $scope.nodes = nodes;
    $scope.edges = edges;

    var draw = function () {
        var container = document.getElementById('mynetwork');
        var data = {
            nodes: $scope.nodes,
            edges: $scope.edges
        };
        var options = {};
        network = new vis.Network(container, data, options);
    };

    $scope.draw = draw;
    $scope.$evalAsync(function () {
        $scope.draw();
    });
}