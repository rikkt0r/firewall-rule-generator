from fw_engine.generator import AbstractGenerator
from fw_engine.models import Host


class Generator(AbstractGenerator):

    def generate_for_rule_module(self, module):

        line = " -m %s" % module.sys

        for param in module.params_set:
            line += " --%s %s" % (param.sys, param.value)

        return line

    def generate_for_rule(self, rule):

        line = "iptables "

        if rule.table is not None:
            line += " -t %s" % rule.get_table_display()

        line += " -A %s" % rule.get_chain_display()

        if rule.protocol is not None:
            line += " %s -p %s" % ('!' if rule.protocol_reverse else '', rule.get_protocol_display())

        if rule.source is not None:
            line += " %s -s %s" % ('!' if rule.source_reverse else '', rule.source)
            if rule.source_mask is not None:
                line += '/%s' % rule.source_mask

        if rule.destination is not None:
            line += " %s -s %s" % ('!' if rule.destination_reverse else '', rule.destination)
            if rule.destination_mask is not None:
                line += '/%s' % rule.destination_mask

        if rule.interface_in:
            line += " %s -i %s" % ('!' if rule.interface_in_reverse else '', rule.interface_in)

        if rule.interface_out:
            line += " %s -o %s" % ('!' if rule.interface_out_reverse else '', rule.interface_out)

        if rule.fragment:
            line += " %s -f" % '!' if rule.fragment == 1 else ''

        if rule.counter:
            line += " -c %s" % rule.get_counter_display()

        for module in rule.modules:
            line += self.generate_for_rule_module(module)

        line += " -j %s" % rule.get_action_display()

        if rule.action == 3 or rule.get_action_display() == 'LOG':  # ten or jako zabezpieczenie przy przypadkowych zmianach..
            if rule.log_level is not None:
                line += " --log-level %d" % rule.log_level

            if rule.log_prefix is not None:
                line += " --log-prefix %s" % rule.log_prefix

        return line

    def generate(self, host_id):

        lines = []

        host = Host.objects.get(pk=host_id)
        template_rules = host.template.rules
        rules = host.rules

        for rule in template_rules:
            lines.append(self.generate_for_rule(rule))

        for rule in rules:
            lines.append(self.generate_for_rule(rule))

        return lines
