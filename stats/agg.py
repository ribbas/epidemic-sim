#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import statistics
from os import listdir, path
import sys

data_dir = sys.argv[1]
stat_features = [
    "severity",
    "infectivity",
    "fatality",
    "birth_rate",
    "cure_threshold",
    "cure_started_day",
    "total_inf",
    "total_dead",
    "days",
]
AGG_STATS = {feature: [x for x in range(48)] for feature in stat_features}


def attr_with_index(attr, data):

    value = attr(data)
    return value, data.index(value)


for f in listdir(data_dir):
    with open(path.join(data_dir, f)) as data_file:
        data = json.load(data_file)
        for feature in stat_features:
            AGG_STATS[feature][int(f[:-5])] = data[feature]

for feature in stat_features:
    print(feature)
    print("mean:", statistics.mean(AGG_STATS[feature]))
    print("min:", attr_with_index(min, AGG_STATS[feature]))
    print("max:", attr_with_index(max, AGG_STATS[feature]))
