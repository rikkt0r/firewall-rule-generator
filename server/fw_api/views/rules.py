# coding: utf-8
from fw_api.views import AbstractRestApi
from fw_engine.models import Rule, Module, ModuleParam


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

        if 'table' in data:
            rule.table = reverse_choice(Rule.TABLES, data['table'])
        if 'chain' in data:
            rule.chain = reverse_choice(Rule.CHAINS, data['chain'])
        if 'action' in data:
            rule.action = reverse_choice(Rule.ACTIONS, data['action'])

        if 'protocol' in data:
            rule.protocol = reverse_choice(Rule.PROTOCOLS, data['protocol'])

        if 'counter' in data:
            rule.counter = reverse_choice(Rule.COUNTERS, data['counter'])

        if 'modules' in data:
            for module in data['modules']:
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
        data = self.get_json(request)

        rule = Rule()
        oid = self.rule_add_or_edit(rule, data, add=True)
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
            for param in module.params:
                param.delete()
            module.delete()
        return self.send_status(200)
