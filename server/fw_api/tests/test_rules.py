# -*- coding: utf-8 -*-
import json
from django.test import SimpleTestCase
from fw_engine.models import Rule, Host


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
