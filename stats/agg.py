#!/usr/bin/env python
# -*- coding: utf-8 -*-

from argparse import ArgumentParser
import json
from os import listdir, path
import statistics

import plotly.graph_objs as go
from plotly.subplots import make_subplots

parser = ArgumentParser()
parser.add_argument("path", type=str)
parser.add_argument("end_seed", type=int, default=0)
parser.add_argument("--plot", "-p", action="store_true", default=False)
parser.add_argument("--dump", "-d", action="store_true", default=False)
args = parser.parse_args().__dict__

data_dir = args["path"]
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
AGG_STATS = {feature: [x for x in range(int(args["end_seed"]) + 1)] for feature in stat_features}

for f in listdir(data_dir):
    with open(path.join(data_dir, f)) as data_file:
        data = json.load(data_file)
        try:
            for feature in stat_features:
                AGG_STATS[feature][int(f[:-5])] = data[feature]
        except IndexError:
            print(f)

if args["dump"]:

    def attr_with_index(attr, data):

        value = attr(data)
        return value, data.index(value)

    for feature in stat_features:
        print(feature)
        print("mean:", statistics.mean(AGG_STATS[feature]))
        print("min:", attr_with_index(min, AGG_STATS[feature]))
        print("max:", attr_with_index(max, AGG_STATS[feature]))

if args["plot"]:

    fig = make_subplots(
        rows=1, cols=2
    )
    fig.add_trace(
        go.Scatter(
            y=AGG_STATS["total_inf"],
            name="Total infected",
            hovertemplate="<b>%{text}</b>",
            text=[
                f"Total infected: {total_inf}<br>" +
                f"Total dead: {total_dead}<br>" +
                f"Severity: {severity}<br>" +
                f"Infectivity: {infectivity}<br>" +
                f"Fatality: {fatality}<br>" +
                f"Birth rate: {birth_rate}<br>" +
                f"Cure threshold: {cure_threshold}<br>" +
                f"Cure Started Day: {cure_started_day}<br>"
                for severity, infectivity, fatality, birth_rate, cure_threshold,
                cure_started_day, total_inf, total_dead, days,
                in zip(*(AGG_STATS[feat] for feat in stat_features))
            ],
            line={"color": "rgb(255,154,0)"},
            mode="markers",
        ),
        row=1, col=1
    )
    fig.add_trace(
        go.Box(
            y=AGG_STATS["total_inf"],
            name="Total infected",
            boxpoints="all", jitter=0.3
        ),
        row=1, col=2
    )

    fig.show()
