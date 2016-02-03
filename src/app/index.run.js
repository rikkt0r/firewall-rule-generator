(function() {
  'use strict';

  angular
    .module('iptables')
    .run(runBlock);

  /** @ngInject */
  function runBlock($log) {

    $log.debug('runBlock end');
  }

})();
