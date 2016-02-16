# coding: utf-8
from fw_api.views import AbstractRestApi
from fw_engine.models import Rule


def reverse_choice(tpl, choice):
    return {v: k for k, v in tpl}[choice]


class RulesApi(AbstractRestApi):

    http_method_names = ['get', 'post', 'put', 'delete']

    def rule_add_or_edit(self, rule, data):

        for f in Rule.FIELDS:
            if data.get(f, None):
                setattr(rule, f, data[f])

        # table, chain, action REQUIRED - so if none present, creates an exception
        rule.table = reverse_choice(Rule.TABLES, data['table'])
        rule.chain = reverse_choice(Rule.CHAINS, data['chain'])
        rule.action = reverse_choice(Rule.ACTIONS, data['action'])

        if 'protocol' in data:
            rule.protocol = reverse_choice(Rule.PROTOCOLS, data['protocol'])

        if 'counter' in data:
            rule.counter = reverse_choice(Rule.COUNTERS, data['counter'])

        if 'modules' in data:
            for module in data['modules']:
                pass
        rule.save()
        return str(rule.id)

    def get(self, request, *args, **kwargs):
        return self.send_json({'implementation': 'needed'})

    def post(self, request, *args, **kwargs):
        data = self.get_json(request)

        rule = Rule()
        oid = self.rule_add_or_edit(rule, data)
        return self.send_json({"id": oid})
