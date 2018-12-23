#!/usr/bin/env python3

import copy
import itertools
import random
import math
from numpy import ndarray
import numpy as np


def _ensure_list(l):
    """ensures that l is list. if not, returns [l]"""
    return l if isinstance(l, (list, ndarray)) else [l]


def add_to_configurations(configs: list, d: dict):
    ds = generate_configurations(d)
    cs = []
    for c, d in itertools.product(configs, ds):
        c = copy.deepcopy(c)
        for k, v in d.items():
            c[k] = v
        cs.append(c)
    return cs


def sample_from_configurations(configs, num_samples):
    return random.sample(configs, num_samples)


def number_of_configs(conf_specs):
    conf_specs = _ensure_list(conf_specs)
    return sum(number_of_configs_single(cs) for cs in conf_specs)


def number_of_configs_single(conf_spec):
    if not len(conf_spec):
        return 0
    n = 1
    for v in conf_spec.values():
        if isinstance(v, (list, ndarray)):
            n *= len(v)
    return n


def generate_configurations(conf_specs, num_samples=-1, shuffle=False):
    conf_specs = _ensure_list(conf_specs)
    configurations = []
    if num_samples < 0:
        for cs in conf_specs:
            confs = generate_configurations_single(cs)
            configurations.extend(confs)
    else:
        nums = np.array([number_of_configs_single(cs) for cs in conf_specs])
        total = np.sum(nums)
        buckets = np.random.choice(len(nums), num_samples, True, nums / total)
        _, counts = np.unique(buckets, return_counts=True)
        for cs, ct in zip(conf_specs, counts):
            confs = generate_configurations_single(cs, ct)
            configurations.extend(confs)
    if shuffle:
        random.shuffle(configurations)
    return configurations


def generate_configurations_single(conf_specs, num_samples=-1):
    """if num_samples is int, then sample that many elements. If it is float, sample that fraction. If it is <= 0, return all elements."""
    configurations = []
    vals = list(map(_ensure_list, conf_specs.values()))
    inds = [list(range(len(v))) for v in vals]

    if not isinstance(num_samples, (int, np.int32, np.int64)):
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
