# -*- coding: utf-8 -*-
import json
from django.test import SimpleTestCase
from fw_engine.models import Host, Template, Interface


class TestHosts(SimpleTestCase):
    def test_get(self):
        host1 = Host()
        host1.name = "lulz"
        host1.htype = 2
        host1.save()

        host2 = Host()
        host2.name = "testu testu"
        host2.interfaces = [Interface()]
        host2.interfaces[0].sys = "eth0"
        host2.interfaces[0].ip = "192.168.5.1"
        host2.interfaces[0].netmask = 24
        host2.save()

        oid1 = str(host1.id)
        oid2 = str(host2.id)

        response = self.client.get('/api/hosts/', follow=True)
        self.assertEqual(200, response.status_code)
        data = response.json()['hosts']

        ids = [host['id'] for host in data]

        self.assertIn(oid1, ids)
        self.assertIn(oid2, ids)

        for host in data:
            if host['id'] == oid1:
                self.assertEqual(host['name'], "lulz")
                self.assertEqual(host['htype'], 2)

            if host['id'] == oid2:
                self.assertEqual(host['name'], "testu testu")
                self.assertEqual(host['interfaces'][0]['sys'], 'eth0')

        host1.delete()
        host2.delete()

    def test_post(self):
        temp = Template()
        temp.name = "Template z testu"
        temp.desc = "bla bla"
        temp.save()

        response = self.client.post('/api/hosts/', data=json.dumps({
            "name": "Host z testu",
            "htype": 3,
            "template_id": str(temp.id),
            "interfaces": [
                {"sys": "eth0", "desc": "gigabit realtek", "ip": "12.11.10.1", "netmask": 24},
                {"sys": "wlan0", "desc": "wireless atheros 2k", "ip": "12.11.9.1", "netmask": 24},
            ]
        }), content_type="application/json", follow=True)

        self.assertEqual(200, response.status_code)
        oid = response.json()['id']

        host = Host.objects.get(pk=oid)
        self.assertEqual(host.name, "Host z testu")
        self.assertEqual(host.htype, 3)
        self.assertEqual(host.interfaces[0].sys, 'eth0')

        host.delete()
        temp.delete()

    def test_put(self):
        host = Host()
        host.name = "Test host update"
        host.save()

        oid = str(host.id)

        response = self.client.put('/api/hosts/%s/' % oid, data=json.dumps({
            "name": "Some other host update name",
            "htype": 2
        }), content_type="application/json", follow=True)

        self.assertEqual(200, response.status_code)

        host = Host.objects.get(pk=oid)
        self.assertEqual(host.htype, 2)
        self.assertEqual(host.name, 'Some other host update name')
        host.delete()

    def test_delete(self):
        host = Host()
        host.name = "Test host delete"
        host.save()

        oid = str(host.id)

        response = self.client.delete('/api/hosts/%s/' % oid, follow=True)
        if response.status_code != 200:
            Host.objects.get(pk=oid).delete()
            self.fail("Didnt delete successfully")
