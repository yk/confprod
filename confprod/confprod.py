import itertools


def _ensure_list(l):
    """ensures that l is list. if not, returns [l]"""
    return l if isinstance(l, list) else [l]


def generate_configurations(conf_specs):
    configurations = []
    if not isinstance(conf_specs, list):
        conf_specs = [conf_specs]
    for conf_object in conf_specs:
        vals = map(_ensure_list, conf_object.values())
        prod = itertools.product(*vals)
        for item in prod:
            conf = dict(zip(conf_object.keys(), item))
            configurations.append(conf)
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
