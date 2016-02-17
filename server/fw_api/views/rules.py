# coding: utf-8
from fw_api.views import AbstractRestApi
from fw_engine.models import Rule, Module, ModuleParam, Host


def reverse_choice(tpl, choice):
    return {v: k for k, v in tpl}[choice]


class RulesApi(AbstractRestApi):

    http_method_names = ['get', 'post', 'put', 'delete']

    def rule_add_or_edit(self, rule, data, add=False):

        for f in Rule.FIELDS:
            if data.get(f, None):
                setattr(rule, f, data[f])

        # table, chain, action REQUIRED
        if add and ('table' not in data or 'chain' not in data or 'action' not in data):
            from fw_common.exceptions import FwException
            raise FwException("Not enough parameters...")

        if 'table' in data and data['table'] is not None:
            rule.table = reverse_choice(Rule.TABLES, data['table'])
        if 'chain' in data and data['chain'] is not None:
            rule.chain = reverse_choice(Rule.CHAINS, data['chain'])
        if 'action' in data and data['action'] is not None:
            rule.action = reverse_choice(Rule.ACTIONS, data['action'])

        if 'protocol' in data and data['protocol'] is not None:
            rule.protocol = reverse_choice(Rule.PROTOCOLS, data['protocol'])

        if 'counter' in data and data['counter'] is not None:
            rule.counter = reverse_choice(Rule.COUNTERS, data['counter'])

        if 'modules' in data:
            for module in data['modules']:
                if not add:
                    # lulz, this library suck, references arent removed even if cascade...
                    found = -1
                    for m in rule.modules:
                        if m.sys == module['sys']:
                            found = rule.modules.index(m)
                            m.delete()
                    if found > -1:
                        del rule.modules[found]
                mod = Module()
                mod.sys = module['sys']
                for param in module['params']:
                    mod.params.append(ModuleParam())
                    mod.params[-1].sys = param['sys']
                    mod.params[-1].value = param['value']
                mod.save()
                rule.modules.append(mod)

        rule.save()
        return str(rule.id)

    def get(self, request, *args, **kwargs):
        return self.send_json({'implementation': 'needed'})

    def post(self, request, *args, **kwargs):
        host_oid = kwargs.get('host_oid', None)
        host = Host.objects.get(pk=host_oid)

        data = self.get_json(request)
        rule = Rule()
        oid = self.rule_add_or_edit(rule, data, add=True)
        host.rules.append(rule)
        host.save()
        return self.send_json({"id": oid})

    def put(self, request, *args, **kwargs):
        oid = kwargs.get('rule_oid', None)
        if oid is None:
            return self.send_status(400)
        data = self.get_json(request)

        rule = Rule.objects.get(pk=oid)
        oid = self.rule_add_or_edit(rule, data)
        return self.send_status(200)

    def delete(self, request, *args, **kwargs):
        oid = kwargs.get('rule_oid', None)
        if oid is None:
            return self.send_status(400)
        rule = Rule.objects.get(pk=oid)
        for module in rule.modules:
            module.delete()
        rule.delete()
        return self.send_status(200)
