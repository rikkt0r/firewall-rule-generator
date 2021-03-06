# -*- coding: utf-8 -*-
from fw_api.views import *
from django.conf.urls import url
# (?P<uuid4>[0-9A-Za-z_\-]+)

urlpatterns = [
    url(r'^hosts/$', hosts.HostsApi.as_view()),
    url(r'^hosts/(?P<host_oid>[0-9a-z]+)/$', hosts.HostsApi.as_view()),

    url(r'^hosts/(?P<host_oid>[0-9a-z]+)/rules/$', rules.RulesApi.as_view()),
    url(r'^hosts/(?P<host_oid>[0-9a-z]+)/rules/(?P<rule_oid>[0-9a-z]+)/$', rules.RulesApi.as_view()),

    url(r'^hosts/(?P<host_oid>[0-9a-z]+)/generate/(?P<mode>(iptables|puppet))/$', generator.GeneratorApi.as_view()),
    url(r'^available/(?P<what>(modules|tables|chains|actions|templates|loglevels))/$', available.AvailableApi.as_view())
]
