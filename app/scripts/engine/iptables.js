var iptables = (function(window, document, undefined){

    var Exception = Error;

    this.Factory = function(rule){
        this.create = function(type) {
            switch(type){
              case 'rule':
                    return new Rule();
              break;

              case 'host':
                    return new Host();
              break;

              case 'template':
                    return new Template();
              default:
                    throw Exception("Nope");
            }
       }
    }

    // objects --------------------------------------------------------------------------------------------------------

    var IP = function(address, network, netmask){
        this.address = address || null;
        this.network = network || '192.168.0.0';
        this.netmask = netmask || '255.255.255.0';

        this.validator = function(ip, net, mask){
            //TODO
            throw Error("Duh, IP/netmask not valid");
        }
    };

    var Interface = function(name, ip) {
      this.name = name || 'eth0';
      this.ip = ip || new IP();
    };

    var Host = function(name) {
        this.name = name || 'Default host name';
        this.interfaces = [];
        this.rules = [];

        this.addInterface = function(interface){
            if(typeof interface !== Interface) {
                throw Error("Couldn't add interface to host");
            }
            this.interfaces.push(interface);
        }

    };

    var RuleModifier = function(name, $name, $value, $values) {
      // przyklad : name: destination port, $name: --dport, $value: 80, $values: int

      // $values = jakie ograniczenia narzucamy, np.
      // int
      // [a, b, c, ,d ] - lista mozliwych pararmetrow.

    };

    var RuleType = function(name, advanced, $name, $modifiers) {
        // itd
    };

    var Rule = function(name, type, from, to) {
        if(!type) {
          throw Error("No rule type specified");
        }
        this.name = name || '';
        this.type = type; // RuleType();
        this.from = from || null; // new IP();
        this.to = to || null;

    };


    var Template = function(name) {
        this.id = 1;
        this.name = name || '';
        this.rules = [];
    };


    // functions ------------------------------------------------------------------------------------------------------

    function _templateList(name_like){
        var templates = [
            new Template('a'),
            new Template('b'),
        ];

        return templates;
    }

    function toImplement(){}

    // public ---------------------------------------------------------------------------------------------------------

    return {
        getObj: Factory.create,
        templateList: _templateList, // (name_like)
        templateGet: toImplement, // (int || Template)

        hostAdd: toImplement, // (name || host_copy_id) - podajemy jesli chcemy kopiowac z innego hosta
        hostAddInterface: toImplement, // (Host || host_id, Interface)
        hostEdit: toImplement, // (Host || host_id)
        hostRemove: toImplement, // (Host || host_id)
        hostList: toImplement, // (name_like)

        ruleAdd: toImplement, // (Host || host_id, Rule)
        ruleEdit: toImplement, // (Host || host_id, rule_id || Rule)
        ruleList: toImplement, // (Host || host_id, name_like)
        ruleGet: toImplement // (Host || host_id, rule_id)


    }
})(window, document, undefined);
