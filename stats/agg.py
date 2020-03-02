#!/usr/bin/env python
# -*- coding: utf-8 -*-

from argparse import ArgumentParser
import json
from os import listdir, path
import statistics

parser = ArgumentParser()
parser.add_argument("path", type=str)
parser.add_argument("end_seed", type=int, default=0)
parser.add_argument("--plot", "-p", action="store_true", default=False)
parser.add_argument("--dump", "-d", action="store_true", default=False)
args = parser.parse_args().__dict__

data_dir = args["path"]

pending_files = []

file_range = range(int(args["end_seed"]) + 1)

for f in file_range:
    if f"{f}.json" not in listdir(data_dir):
        pending_files.append(str(f))

if pending_files:
    with open("stats/pending.txt", "w") as pending_file:
        print(f"Files pending: {' '.join(pending_files)}")
        pending_file.write("\n".join(pending_files))


stat_features = [
    "seed",
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
        seed = int(f[:-5])
        AGG_STATS["seed"][seed] = seed
        try:
            for feature in stat_features[1:]:
                AGG_STATS[feature][seed] = data[feature]
        except IndexError:
            print(f)

if args["dump"]:

    def attr_with_index(attr, data):

        value = attr(data)
        return value, data.index(value)

    for feature in stat_features[1:]:
        print(feature)
        print("mean:", statistics.mean(AGG_STATS[feature]))
        print("min:", attr_with_index(min, AGG_STATS[feature]))
        print("max:", attr_with_index(max, AGG_STATS[feature]))

if args["plot"]:

    import plotly
    from plotly.subplots import make_subplots

    _text = [
        f"Seed: {seed}<br>" +
        f"Total infected: {total_inf}<br>" +
        f"Total dead: {total_dead}<br>" +
        f"Severity: {severity}<br>" +
        f"Infectivity: {infectivity}<br>" +
        f"Fatality: {fatality}<br>" +
        f"Birth rate: {birth_rate}<br>" +
        f"Cure threshold: {cure_threshold}<br>" +
        f"Cure Started Day: {cure_started_day}<br>"
        for seed, severity, infectivity, fatality, birth_rate, cure_threshold,
        cure_started_day, total_inf, total_dead, days,
        in zip(*(AGG_STATS[feat] for feat in stat_features))
    ]
    fig = make_subplots(
        rows=1, cols=2,
        column_widths=[0.75, 0.25],
        shared_yaxes=True, horizontal_spacing=0.02
    )
    fig.add_trace(
        plotly.graph_objs.Scatter(
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
        plotly.graph_objs.Box(
            y=AGG_STATS["total_inf"],
            name="Distribution of Total Population Infected",
            text=_text,
            jitter=0.3
        ),
        row=1, col=2
    )
    fig.update_layout(
        # title="Plot Title",
        xaxis_title="Days Until Cure Started",
        yaxis_title="Total Population Infected",
        showlegend=False,
    )
    plotly.offline.plot(fig, filename="stats/plot.html", auto_open=False)
