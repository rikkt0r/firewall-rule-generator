# coding: utf-8
from fw_api.views import AbstractRestApi


class GeneratorApi(AbstractRestApi):

    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        host_oid = kwargs.get('host_oid', None)
        if not host_oid:
            return self.send_status(400)

        return getattr(self, 'get_%s' % kwargs.get('mode'))(host_oid)

    # ------------------------------------------------------------------------------------------------------------------

    def get_iptables(self, host_oid):

        from fw_engine_iptables.generator import Generator
        gen = Generator()

        return self.send_json({"lines": gen.generate(host_oid)})

    def get_puppet(self, host_oid):
        return self.send_json({"lines": ["Not available"]})
