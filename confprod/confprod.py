import itertools


class Parameterized:
    def __init__(self, parameters=None):
        if parameters is None: parameters = dict()
        self.parameters = parameters

    def get_parameter(self, name):
        return self.parameters[name]

    def get_parameter_or_default(self, name, default):
        return self.parameters[name] if name in self.parameters else default


def generate_configurations(conf_objects):
    configurations = []
    for conf_object in conf_objects:
        partlists = {}
        for partkey, partlist in conf_object.items():
            partlists[partkey] = []
            if not isinstance(partlist, list):
                partlist = [partlist]
            for parttpl in partlist:
                if not isinstance(parttpl, tuple):
                    parttpl = tuple((parttpl,))
                if len(parttpl) == 1:
                    parttpl = tuple(parttpl[0], dict())
                clazz, param_dict = parttpl
                param_keys, param_lists = zip(*param_dict.items()) if len(param_dict) > 0 else ([], [])
                param_lists = tuple(l if isinstance(l, list) else [l] for l in param_lists)
                param_prods = itertools.product(*param_lists)
                for param_prod in param_prods:
                    parameters = dict(zip(param_keys, param_prod))
                    partlists[partkey].append((clazz, parameters))
        part_keys, part_lists = zip(*partlists.items()) if len(partlists) > 0 else ([], [])
        part_prods = itertools.product(*part_lists)
        for part_prod in part_prods:
            parts = dict(zip(part_keys, part_prod))
            configurations.append(parts)
    return configurations


def instantiate_configuration(configuration):
    conf = {}
    for key, val in configuration.items():
        conf[key] = val[0](val[1])
    return conf


def merge_with_defaults(conf, defaults):
    for key, val in conf.items():
        if key in defaults:
            de = defaults[key]
            if val[0] in de:
                vd = val[1]
                dd = de[val[0]]
                for ddkey, ddval in dd.items():
                    if ddkey not in vd:
                        vd[ddkey] = ddval
    for key, val in defaults.items():
        if key not in conf:
            if isinstance(val, dict):
                if "default" in val:
                    c = val["default"]
                    conf[key] = (c, val[c])
                else:
                    ci = val.items()[0]
                    conf[key] = ci
            else:
                conf[key] = val
    return conf


def generate_instantiated_configurations(conf_objects, defaults=None):
    if defaults is None:
        defaults = dict()
    for conf_object in conf_objects:
        co = merge_with_defaults(conf_object, defaults)
        yield instantiate_configuration(co)

