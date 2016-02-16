# coding: utf-8
from fw_api.views import AbstractRestApi
from fw_engine.models import Module


class AvailableApi(AbstractRestApi):

    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        return getattr(self, 'get_%s' % kwargs.get('what'))()

    # ------------------------------------------------------------------------------------------------------------------

    def get_modules(self):

        modules = Module.objects.all()

        ret = {'modules': []}

        for module in modules:
            m = {
                "sys": module.sys,
                "desc": module.desc,
                "params_available": []
            }

            for p in module.params_available:
                m['params_available'].append({
                    "sys": p.sys,
                    "desc": p.desc
                })

            ret['modules'].append(m)

        return self.send_json(ret)

    def get_chains(self):
        return self.send_json({
            "chains": [
                {"sys": "INPUT", "advanced": False},
                {"sys": "OUTPUT", "advanced": False},
                {"sys": "FORWARDING", "advanced": True},
                {"sys": "PREROUTING", "advanced": True},
                {"sys": "POSTROUTING", "advanced": True},
            ]
        })

    def get_tables(self):
        return self.send_json({
            "tables": [
                {"sys": "filter", "advanced": False},
                {"sys": "mangle", "advanced": True},
                {"sys": "nat", "advanced": True},
                {"sys": "raw", "advanced": True},
                {"sys": "security", "advanced": True},
            ]
        })

    def get_actions(self):
        return self.send_json({
            "actions": [
                {"sys": "DROP", "advanced": False},
                {"sys": "ACCEPT", "advanced": False},
                {"sys": "REJECT", "advanced": False},
                {"sys": "MASQUERADE", "advanced": True},
            ]
        })
