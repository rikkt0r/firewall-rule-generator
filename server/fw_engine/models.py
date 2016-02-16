from __future__ import unicode_literals

from django.core.exceptions import ValidationError
from django.conf import settings
import mongoengine as me

from fw_common.validators import validate_ip, validate_netmask


class Interface(me.EmbeddedDocument):
    FIELDS = ('sys', 'desc', 'ip', 'netmask')

    sys = me.StringField(max_length=8, required=True)
    desc = me.StringField(max_length=80)
    ip = me.StringField(max_length=15, required=True)
    netmask = me.IntField(required=True)

    def clean(self):
        validate_ip(self.ip)
        validate_netmask(self.netmask)
        super(Interface, self).clean()


class Template(me.Document):
    name = me.StringField(max_length=100)
    desc = me.StringField(max_length=300)
    ruleset = me.SortedListField(me.EmbeddedDocumentField('Rule'))


class Host(me.Document):

    FIELDS = ('name', 'htype')

    TYPES = (
        (0, 'PC/Laptop'),
        (1, 'Server'),
        (2, 'Firewall'),
        (3, 'Other')
    )

    name = me.StringField(max_length=100, required=True)
    htype = me.IntField(choices=TYPES, default=0)
    interfaces = me.ListField(me.EmbeddedDocumentField(Interface))
    template = me.ReferenceField(Template)
    rules = me.SortedListField(me.EmbeddedDocumentField('Rule'))

    def __repr__(self):
        return "Host <%s>" % self.name


class ModuleParams(me.EmbeddedDocument):
    sys = me.StringField(max_length=16, required=True)
    desc = me.StringField(max_length=120)
    value = me.StringField(min_length=1, max_length=60)


class Module(me.Document):
    sys = me.StringField(max_length=40)
    desc = me.StringField(max_length=100)
    params_available = me.ListField(me.EmbeddedDocumentField(ModuleParams))
    params_set = me.ListField(me.EmbeddedDocumentField(ModuleParams))


class Rule(me.EmbeddedDocument):
    TABLES = [(i, t[0]) for i, t in enumerate(settings.TABLES)]
    CHAINS = [(i, c[0]) for i, c in enumerate(settings.CHAINS)]
    ACTIONS = [(i, a[0]) for i, a in enumerate(settings.ACTIONS)]

    PROTOCOLS = (
        (0, 'tcp'),
        (1, 'udp'),
        (2, 'icmp')
    )

    FRAGMENT = (
        (0, 'None'),
        (1, 'Yes'),
        (2, 'No')
    )

    COUNTERS = (
        (0, 'None'),
        (1, 'pkts'),
        (2, 'bytes'),
        (3, 'pkts bytes')
    )

    table = me.IntField(choices=TABLES, default=0)
    chain = me.IntField(choices=CHAINS, required=True)
    protocol = me.IntField(choices=PROTOCOLS)
    protocol_reverse = me.BooleanField(default=False)
    source = me.StringField(max_length=15)
    source_mask = me.IntField(default=0)
    source_reverse = me.BooleanField(default=False)
    destination = me.StringField(max_length=15)
    destination_mask = me.IntField(default=0)
    destination_reverse = me.BooleanField(default=False)
    interface_in = me.EmbeddedDocumentField(Interface)
    interface_in_reverse = me.BooleanField(default=False)
    interface_out = me.EmbeddedDocumentField(Interface)
    interface_out_reverse = me.BooleanField(default=False)
    fragment = me.IntField(choices=FRAGMENT, default=0)
    counter = me.IntField(choices=COUNTERS, default=0)
    modules = me.ListField(me.ReferenceField(Module))
    action = me.IntField(choices=ACTIONS, default=0)

    def validate(self, clean=True):
        validate_netmask(self.source_mask)
        validate_netmask(self.destination_mask)
        super(Rule, self).validate(clean)

    #     if self.protocol == 2 and Module.objects.get(sys='multiport') in self.modules:
    #         raise ValidationError("ICMP doesnt provide multiport")
