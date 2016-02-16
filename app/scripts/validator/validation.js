(function() {
  angular
    .module('validation.rule', ['validation'])
    .config(['$validationProvider', function($validationProvider) {
      var expression = {
        required: function(value) {
          return !!value;
        },
        email: /^([\w-\.]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([\w-]+\.)+))([a-zA-Z]{2,4}|[0-9]{1,3})(\]?)$/,
        number: /^\d+$/,
        ip: /^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$/,
        minlength: function(value, scope, element, attrs, param) {
          return value.length >= param;
        },
        maxlength: function(value, scope, element, attrs, param) {
          return value.length <= param;
        }
      };

      var defaultMsg = {
        required: {
          error: 'This fild is mandatory'
        },
        email: {
          error: 'This should be Email'
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
    }]);
}).call(this);
