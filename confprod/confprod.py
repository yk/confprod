#!/usr/bin/env python3

import itertools
import random
import math
from numpy import ndarray


def _ensure_list(l):
    """ensures that l is list. if not, returns [l]"""
    return l if isinstance(l, (list, ndarray)) else [l]


def add_to_configurations(configs: list, d: dict):
    for c in configs:
        for k, v in d.items():
            c[k] = v


def sample_from_configurations(configs, num_samples):
    return random.sample(configs, num_samples)


def generate_configurations(conf_specs, num_samples=-1):
    """if num_samples is int, then sample that many elements. If it is float, sample that fraction. If it is <= 0, return all elements."""
    configurations = []
    vals = list(map(_ensure_list, conf_specs.values()))
    inds = [list(range(len(v))) for v in vals]

    if not isinstance(num_samples, int):
        num_samples = math.ceil(len(configurations) * num_samples)

    if num_samples <= 0:
        prod = itertools.product(*vals)
    else:
        prod = []
        for _ in range(num_samples):
            prod_ind = [random.choice(ind) for ind in inds]
            prod.append([v[i] for v, i in zip(vals, prod_ind)])

    for item in prod:
        conf = dict(zip(conf_specs.keys(), item))
        configurations.append(conf)
    return configurations


def _main():
    import json
    conf_specs = {
            "a": [1,2],
            "b": [3,4],
            "c": 5,
            }
    print(json.dumps(generate_configurations(conf_specs, 3)))

if __name__ == '__main__':
    _main()
