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

PENDING_FILES = []

file_range = range(int(args["end_seed"]) + 1)

for f in file_range:
    if f"{f}.json" not in listdir(data_dir):
        PENDING_FILES.append(str(f))

with open("stats/pending.txt", "w") as pending_file:
    print("Files pending:", PENDING_FILES)
    pending_file.write("\n".join(PENDING_FILES))


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
AGG_STATS = {feature: [x for x in file_range] for feature in stat_features}

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

    _text = [
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
    ]
    fig = make_subplots(
        rows=1, cols=2
    )
    fig.add_trace(
        go.Scatter(
            x=AGG_STATS["cure_started_day"],
            y=AGG_STATS["total_inf"],
            name="Total Population Infected vs Days Until Cure Started",
            hovertemplate="<b>%{text}</b>",
            text=_text,
            line={"color": "rgb(255,154,0)"},
            mode="markers",
        ),
        row=1, col=1
    )
    fig.add_trace(
        go.Box(
            y=AGG_STATS["total_inf"],
            name="Distribution of Total Population Infected",
            text=_text,
            boxpoints="all", jitter=0.3
        ),
        row=1, col=2
    )
    fig.update_layout(
        # title="Plot Title",
        xaxis_title="Days Until Cure Started",
        yaxis_title="Total Population Infected",
        showlegend=False,
    )
    fig.show()
