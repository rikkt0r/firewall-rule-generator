# -*- coding: utf-8 -*-
import json
from django.test import SimpleTestCase
from fw_engine.models import Rule, Host, Module, ModuleParam


class TestRules(SimpleTestCase):
    def test_get(self):
        pass
        # host = Host()
        # host.name = "host for testing rule list"
        # host.save()
        #
        # host_oid = str(host.id)
        #
        # response = self.client.get('/api/hosts/%s/rules/' % host_oid, follow=True)
        # self.assertEqual(200, response.status_code)
        # data = response.json()['rules']
        #
        # ids = [r['id'] for r in data]
        #
        # host.delete()

    def test_post(self):

        host = Host()
        host.name = "test host for rules"
        host.save()

        response = self.client.post('/api/hosts/%s/rules/' % str(host.id), data=json.dumps({
            "table": "filter",
            "chain": "INPUT",
            "protocol": "tcp",
            "interface_in": "eth0",
            "modules": [
              {"sys": "state", "params": [
                {"sys": "state", "value": "RELATED,ESTABLISHED"},
              ]},
            ],
            "action": "LOG",
            "log_level": 4,
            "log_prefix": "Log established"
        }), content_type="application/json", follow=True)

        self.assertEqual(200, response.status_code)
        rule_oid = response.json()['id']

        rule = Rule.objects.get(pk=rule_oid)
        self.assertEqual(rule.table, 0)
        self.assertEqual(rule.chain, 0)
        self.assertEqual(rule.modules[0].sys, 'state')
        self.assertEqual(rule.modules[0].params[0].value, 'RELATED,ESTABLISHED')

        rule.modules[0].delete()
        rule.delete()
        host.delete()

    def test_put(self):

        host = Host()
        host.name = "test host for rules"
        host.save()

        mod = Module()
        mod.sys = "limit"
        mod.params.append(ModuleParam())
        mod.params[0].sys = "limit-rate"
        mod.params[0].value = "5/min"
        mod.save()

        rule = Rule()
        rule.chain = 0
        rule.action = 0
        rule.source = '192.168.0.1'
        rule.source_mask = 24
        rule.source_reverse = True
        rule.modules.append(mod)
        rule.save()

        host.rules.append(rule)
        host.save()

        response = self.client.put('/api/hosts/%s/rules/%s/' % (str(host.id), str(rule.id)), data=json.dumps({
            "chain": "OUTPUT",
            "protocol": "tcp",
            "interface_in": "eth0",
            "modules": [
              {"sys": "state", "params": [
                {"sys": "state", "value": "RELATED,ESTABLISHED"},
              ]},
              {"sys": "limit", "params": [
                {"sys": "limit-rate", "value": "100/s"},
                {"sys": "limit-burst", "value": "500/s"},
              ]},
            ]
        }), content_type="application/json", follow=True)

        self.assertEqual(200, response.status_code)
        rule = Rule.objects.get(pk=str(rule.id))  # pobieram zeby odswiezyc obiekt, nie ma funkcji sync czy cokolwiek.

        self.assertEqual(rule.table, 0)
        self.assertEqual(rule.chain, 1)
        self.assertEqual(rule.modules[0].sys, 'state')
        self.assertEqual(rule.modules[0].params[0].value, 'RELATED,ESTABLISHED')
        self.assertEqual(rule.modules[1].sys, 'limit')
        self.assertEqual(rule.modules[1].params[0].sys, 'limit-rate')
        self.assertEqual(rule.modules[1].params[1].sys, 'limit-burst')
        self.assertEqual(rule.modules[1].params[0].value, '100/s')
        self.assertEqual(rule.modules[1].params[1].value, '500/s')

        for mod in rule.modules:
            mod.delete()
        rule.delete()
        host.delete()

    def test_delete(self):
        host = Host()
        host.name = "test host for rules"
        host.save()

        mod = Module()
        mod.sys = "limit"
        mod.params.append(ModuleParam())
        mod.params[0].sys = "limit-rate"
        mod.params[0].value = "5/min"
        mod.save()

        rule = Rule()
        rule.chain = 0
        rule.action = 0
        rule.source = '192.168.0.1'
        rule.source_mask = 24
        rule.source_reverse = True
        rule.modules.append(mod)
        rule.save()

        host.rules.append(rule)
        host.save()

        oid = str(host.id)

        response = self.client.delete('/api/hosts/%s/rules/%s/' % (str(host.id), str(rule.id)), follow=True)
        host.delete()

        if response.status_code != 200:
            Host.objects.get(pk=oid).delete()
            rule.delete()
            self.fail("Didnt delete successfully")
