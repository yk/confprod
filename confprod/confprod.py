import itertools
import random
import math


def _ensure_list(l):
    """ensures that l is list. if not, returns [l]"""
    return l if isinstance(l, list) else [l]


def add_to_configurations(configs: list, d: dict):
    for c in configs:
        for k, v in d.items():
            c[k] = v


def sample_from_configurations(configs, num_samples):
    return random.sample(configs, num_samples)


def generate_configurations(conf_specs, num_samples=-1):
    """if num_samples is int, then sample that many elements. If it is float, sample that fraction. If it is <= 0, return all elements."""
    configurations = []
    if not isinstance(conf_specs, list):
        conf_specs = [conf_specs]
    for conf_object in conf_specs:
        vals = map(_ensure_list, conf_object.values())
        prod = itertools.product(*vals)
        for item in prod:
            conf = dict(zip(conf_object.keys(), item))
            configurations.append(conf)
    if num_samples > 0:
        if not isinstance(num_samples, int):
            num_samples = math.ceil(len(configurations) * num_samples)
        configurations = sample_from_configurations(configurations, num_samples)
    return configurations


def _main():
    import json
    conf_specs = [
            {
            "a": [1,2],
            "b": [3,4],
            "c": 5,
            },
            {
                "a": 1,
                "b": [3,4]
                }
            ]
    print(json.dumps(generate_configurations(conf_specs)))

if __name__ == '__main__':
    _main()
