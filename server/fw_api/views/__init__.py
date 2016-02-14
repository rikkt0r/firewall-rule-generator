# coding: utf-8

import json
from django.http import JsonResponse
from django.views.generic import View
from fw_common.exceptions import FwException

__all__ = ['hosts', 'rules']


class AbstractRestApi(View):

    http_method_names = ['get', 'post', 'put', 'delete']

    def __init__(self, **kwargs):
        super(AbstractRestApi, self).__init__(**kwargs)
        for key, value in kwargs.iteritems():
            setattr(self, key, value)

    def get(self, request, *args, **kwargs):
        pass

    def post(self, request, *args, **kwargs):
        pass

    def put(self, request, *args, **kwargs):
        pass

    def delete(self, request, *args, **kwargs):
        pass

    def send_error(self, error, status_code):
        response = JsonResponse(error)
        response.status_code = status_code
        return response

    def get_json(self, request):

        data = getattr(request, 'body', None)

        if data is None:
            raise FwException('Error occurred: No incoming data')

        if len(data) > 1000:
            raise FwException('Error occurred: Impossibly long json..')

        try:
            return json.loads(data.decode("utf-8"))
        except (UnicodeEncodeError, ValueError, TypeError, KeyError, AttributeError):
            raise FwException('Error occurred: Invalid incoming JSON')

    def send_json(self, obj):
        return JsonResponse(obj)

    def send_status(self, status_code):
        from django.http import HttpResponse
        return HttpResponse(status=status_code)
