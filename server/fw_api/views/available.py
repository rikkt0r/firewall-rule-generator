# coding: utf-8
from django.conf import settings
from fw_api.views import AbstractRestApi
from fw_engine.models import Template, ModuleAvailable


class AvailableApi(AbstractRestApi):

    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        return getattr(self, 'get_%s' % kwargs.get('what'))()

    # ------------------------------------------------------------------------------------------------------------------

    def get_modules(self):

        modules = ModuleAvailable.objects.all()

        ret = {'modules': []}

        for module in modules:
            m = {
                "sys": module.sys,
                "desc": module.desc,
                "params": []
            }

            for p in module.params:
                m['params'].append({
                    "sys": p.sys,
                    "desc": p.desc
                })

            ret['modules'].append(m)

        return self.send_json(ret)

    def get_chains(self):
        return self.send_json({"chains": [{"sys": c[0], "advanced": c[1]} for c in settings.CHAINS]})

    def get_tables(self):
        return self.send_json({"tables": [{"sys": c[0], "advanced": c[1]} for c in settings.TABLES]})

    def get_actions(self):
        return self.send_json({"actions": [{"sys": c[0], "advanced": c[1]} for c in settings.ACTIONS]})

    def get_loglevels(self):
        return self.send_json({"loglevels": [{c[1]: c[0]} for c in settings.LOG_LEVELS]})

    def get_templates(self):
        templates = Template.objects.all()
        data = {'templates': []}

        for template in templates:
            data['templates'].append({"id": str(template.id), "name": template.name, "desc": template.desc})
        return self.send_json(data)
