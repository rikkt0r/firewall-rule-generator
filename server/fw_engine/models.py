from __future__ import unicode_literals

from django.core.exceptions import ValidationError
from django.conf import settings
import mongoengine as me
# from mongoengine.queryset import CASCADE

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

    def __repr__(self):
        return "Interface <%s>" % self.sys


class Template(me.Document):
    name = me.StringField(max_length=100)
    desc = me.StringField(max_length=300)
    rules = me.SortedListField(me.ReferenceField('Rule'))

    def __repr__(self):
        return "Template <%s>" % self.name


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
    rules = me.SortedListField(me.ReferenceField('Rule'))

    def __repr__(self):
        return "Host <%s>" % self.name


class ModuleAvailableParams(me.EmbeddedDocument):
    sys = me.StringField(max_length=16, required=True)
    desc = me.StringField(max_length=120)


class ModuleAvailable(me.Document):
    sys = me.StringField(max_length=40)
    desc = me.StringField(max_length=100)
    params = me.ListField(me.EmbeddedDocumentField(ModuleAvailableParams))

    def __repr__(self):
        return "ModuleAvailable <%s>" % self.sys


class ModuleParam(me.EmbeddedDocument):
    sys = me.StringField(max_length=16, required=True)
    value = me.StringField(min_length=1, max_length=60)


class Module(me.Document):
    sys = me.StringField(max_length=40)
    params = me.ListField(me.EmbeddedDocumentField(ModuleParam))

    def __repr__(self):
        return "Module <%s>" % self.sys


class Rule(me.Document):
    TABLES = [(i, t[0]) for i, t in enumerate(settings.TABLES)]
    CHAINS = [(i, c[0]) for i, c in enumerate(settings.CHAINS)]
    ACTIONS = [(i, a[0]) for i, a in enumerate(settings.ACTIONS)]
    LOG_LEVELS = settings.LOG_LEVELS

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

    FIELDS = ('protocol_reverse', 'source', 'source_mask', 'source_reverse', 'destination', 'destination_mask',
              'destination_reverse', 'interface_in', 'interface_in_reverse', 'fragment', 'log_level', 'log_prefix')
    # table, chain, protocol, counter, modules, action

    table = me.IntField(choices=TABLES, default=0, required=True)
    chain = me.IntField(choices=CHAINS, required=True)
    protocol = me.IntField(choices=PROTOCOLS)
    protocol_reverse = me.BooleanField(default=False)
    source = me.StringField(max_length=15)
    source_mask = me.IntField(default=0)
    source_reverse = me.BooleanField(default=False)
    destination = me.StringField(max_length=15)
    destination_mask = me.IntField(default=0)
    destination_reverse = me.BooleanField(default=False)
    interface_in = me.StringField(max_length=8)
    interface_in_reverse = me.BooleanField(default=False)
    interface_out = me.StringField(max_length=8)
    interface_out_reverse = me.BooleanField(default=False)
    fragment = me.IntField(choices=FRAGMENT, default=0)
    counter = me.IntField(choices=COUNTERS, default=0)
    # modules = me.ListField(me.ReferenceField(Module, reverse_delete_rule=CASCADE))
    modules = me.ListField(me.ReferenceField(Module))
    action = me.IntField(choices=ACTIONS, required=False)
    log_level = me.IntField(choices=LOG_LEVELS)
    log_prefix = me.StringField(max_length=40)

    def validate(self, clean=True):
        validate_netmask(self.source_mask)
        validate_netmask(self.destination_mask)
        if self.protocol == 2:
            for m in self.modules:
                if m.sys == 'multiport':
                    raise ValidationError("ICMP is not compatible with multiport")
        super(Rule, self).validate(clean)

    def __deepcopy__(self):
        fields = self.FIELDS + ('table', 'chain', 'protocol', 'counter', 'action')
        rule = Rule()
        for f in fields:
            setattr(rule, f, getattr(self, f))
        for m in self.modules:
            rule.modules.append(m)
        return rule

    def __repr__(self):
        return "Rule <%s, modules: %d>" % (self.get_action_display(), len(self.modules))
