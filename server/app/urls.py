# coding: utf-8

from django.conf.urls import url, include
# from django.contrib import admin
from django.views.generic import TemplateView

urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^$', TemplateView.as_view(template_name='index.html'), name='index'),
    url(r'^api/', include('fw_api.urls', namespace='api')),
]

handler404 = "fw_common.views.handler404"
handler500 = "fw_common.views.handler500"
