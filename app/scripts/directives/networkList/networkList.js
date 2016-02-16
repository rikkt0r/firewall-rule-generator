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
function networkListCtrl($scope, $uibModal) {

    function ModalInstanceCtrl($scope, IpTablesService, $uibModalInstance, Host, Hosts) {

        $scope.host = Host;

        $scope.confirm = function () {
            IpTablesService.removeHost(Host.id)
                .then(
                    function(){
                        $uibModalInstance.dismiss('removed');
                        Hosts = IpTablesService.getHosts(true);
                    }
                )
        };

        $scope.cancel = function () {
            $uibModalInstance.dismiss('cancel');
        };
    }

    $scope.confirmDelete = function (host) {
        var modalInstance = $uibModal.open({
            animation: $scope.animationsEnabled,
            scope: $scope,
            templateUrl: 'delete-confirmation-modal.html',
            size: 'small',
            controller: ModalInstanceCtrl,
            resolve: {
                Host: function () {
                    return host;
                },
                Hosts: function () {
                    return $scope.hosts;
                }
            }
        });

        modalInstance.result.then(function (selectedItem) {
        }, function () {
        });
    };

    $scope.toggleAnimation = function () {
        $scope.animationsEnabled = !$scope.animationsEnabled;
    };

    $scope.getType = function(typeId) {
        switch(typeId){
            case 1: return 'PC/Laptop';
            case 2: return 'Server';
            case 3: return 'Firewall';
            default: return 'Other';
        }
    }
}
