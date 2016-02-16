# coding: utf-8
import json
from fw_api.views import AbstractRestApi
from fw_engine.models import Host, Template, Interface


class HostsApi(AbstractRestApi):

    http_method_names = ['get', 'post', 'put', 'delete']

    def host_add_or_edit(self, host, data):

        for f in Host.FIELDS:
            if data.get(f, None):
                setattr(host, f, data[f])

        if 'template_id' in data:
            temp = Template.objects.get(pk=data['template_id'])
            host.template = temp

        if 'interfaces' in data:
            for interface in host.interfaces:
                interface.delete()
            for interface in data['interfaces']:
                host.interfaces.append(Interface())
                for f in Interface.FIELDS:
                    if interface.get(f, None):
                        setattr(host.interfaces[-1], f, interface[f])
        host.save()
        return str(host.id)

    # ------------------------------------------------------------------------------------------------------------------

    def get(self, request, *args, **kwargs):
        hosts = Host.objects.all()
        data = {'hosts': []}
        for host in hosts:
            data['hosts'].append({
                "id": str(host.id),
                "htype": host.htype,
                "name": host.name,
                "interfaces": [json.loads(i.to_json()) for i in host.interfaces],
                "template_name": host.template.name if host.template else None
            })

        return self.send_json(data)

    def post(self, request, *args, **kwargs):
        data = self.get_json(request)

        host = Host()
        oid = self.host_add_or_edit(host, data)
        return self.send_json({"id": oid})

    def put(self, request, *args, **kwargs):
        oid = kwargs.get('host_oid', None)
        if oid is None:
            return self.send_status(400)
        data = self.get_json(request)

        host = Host.objects.get(pk=oid)
        oid = self.host_add_or_edit(host, data)
        return self.send_status(200)

    def delete(self, request, *args, **kwargs):
        oid = kwargs.get('host_oid', None)
        if oid is None:
            return self.send_status(400)
        host = Host.objects.get(pk=oid)
        for interface in host.interfaces:
            interface.delete()
        return self.send_status(200)
