class AbstractGenerator(object):

    def generate(self, host_id):
        raise NotImplementedError()

    def generate_for_rule_module(self, module):
        raise NotImplementedError()

    def generate_for_rule(self, rule):
        raise NotImplementedError()
