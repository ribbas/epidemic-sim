#!/usr/bin/env python
# -*- coding: utf-8 -*-

from argparse import ArgumentParser
import sqlite3
import statistics

parser = ArgumentParser()
parser.add_argument("path", type=str)
parser.add_argument("end_seed", type=int, default=0)
parser.add_argument("--plot", "-p", action="store_true", default=False)
parser.add_argument("--dump", "-d", action="store_true", default=False)
args = parser.parse_args().__dict__

data_dir = args["path"]
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

conn = sqlite3.connect(data_dir)

db = []

for row in conn.execute("SELECT * FROM STATS WHERE SEED < 2048"):
    db.append(dict(zip(stat_features, row)))

db = {k: [d[k] for d in db if k in d] for k in stat_features}

conn.close()

if args["dump"]:

    def attr_with_index(attr, data):

        value = attr(data)
        return value, data.index(value)

    for feature in stat_features[1:]:
        print("---------------------------------------")
        print(feature)
        print("mean:", statistics.mean(db[feature]))
        print("median:", statistics.median(db[feature]))
        print("min:", attr_with_index(min, db[feature]))
        print("max:", attr_with_index(max, db[feature]))
        print("---------------------------------------")

if args["plot"]:

    import plotly
    from plotly.subplots import make_subplots

    _text = [
        f"Seed: {db['seed'][x]}<br>" +
        f"Total infected: {db['total_inf'][x]}<br>" +
        f"Total dead: {db['total_dead'][x]}<br>" +
        f"Severity: {db['severity'][x]}<br>" +
        f"Infectivity: {db['infectivity'][x]}<br>" +
        f"Fatality: {db['fatality'][x]}<br>" +
        f"Birth rate: {db['birth_rate'][x]}<br>" +
        f"Cure threshold: {db['cure_threshold'][x]}<br>" +
        f"Cure Started Day: {db['cure_started_day'][x]}<br>"
        f"Days: {db['days'][x]}<br>"
        for x in range(int(args["end_seed"]) + 1)
    ]

    fig = make_subplots(
        rows=1, cols=2,
        column_widths=[0.75, 0.25],
        shared_yaxes=True, horizontal_spacing=0.02
    )
    fig.add_trace(
        plotly.graph_objs.Scatter(
            x=db["cure_started_day"],
            y=db["total_inf"],
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
            y=db["total_inf"],
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
