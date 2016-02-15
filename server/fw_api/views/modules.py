# coding: utf-8
from fw_api.views import AbstractRestApi


class ModulesApi(AbstractRestApi):

    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        from fw_engine.models import Module
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
