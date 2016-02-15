angular
    .module('yapp')
    .directive('networkList', networkList);

/** @ngInject */
function networkList() {
    var directive = {
        restrict: 'E',
        templateUrl: 'scripts/directives/networkList/network-list.html',
        scope: {
            hosts: '='
        },
        controller: networkListCtrl,
        controllerAs: 'vm',
    };

    return directive;
}

/** @ngInject */
function networkListCtrl($scope, IpTablesService) {

}