from __future__ import unicode_literals

from django.core.exceptions import ValidationError
import mongoengine as me

from fw_common.validators import validate_ip, validate_netmask


class Interface(me.EmbeddedDocument):
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


class ModuleParams(me.EmbeddedDocument):
    sys = me.StringField(max_length=16)
    desc = me.StringField(max_length=80)
    value = me.StringField(min_length=1, max_length=60)


class Module(me.EmbeddedDocument):
    sys = me.StringField(max_length=40)
    desc = me.StringField(max_length=80)
    params_available = me.ListField(me.EmbeddedDocumentField(ModuleParams))
    params_set = me.ListField(me.EmbeddedDocumentField(ModuleParams))


class Rule(me.EmbeddedDocument):
    TABLES = (
        (0, 'filter'),
        (1, 'raw'),
        (2, 'mangle'),
        (3, 'nat'),
        (4, 'security')
    )

    CHAINS = (
        (0, 'INPUT'),
        (1, 'OUTPUT')
    )

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
    interface_out = me.EmbeddedDocumentField(Interface)
    fragment = me.IntField(choices=FRAGMENT, default=0)
    counter = me.IntField(choices=COUNTERS, default=0)
    modules = me.ListField(me.EmbeddedDocumentField(Module))

    def validate(self, clean=True):
        validate_netmask(self.source_mask)
        validate_netmask(self.destination_mask)
        super(Rule, self).validate(clean)

    #     if self.protocol == 2 and Module.objects.get(sys='multiport') in self.modules:
    #         raise ValidationError("ICMP doesnt provide multiport")
