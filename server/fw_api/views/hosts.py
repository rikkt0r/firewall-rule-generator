# coding: utf-8
from fw_api.views import AbstractRestApi


class HostsApi(AbstractRestApi):

    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        return self.send_json({'implementation': 'needed'})
