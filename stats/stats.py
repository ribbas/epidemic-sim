#!/usr/bin/env python
# -*- coding: utf-8 -*-

from argparse import ArgumentParser
import json
from os import listdir, path
import sqlite3

parser = ArgumentParser()
parser.add_argument("path", type=str)
parser.add_argument("--end_seed", "-e", type=int, default=0)
parser.add_argument("--begin_seed", "-b", type=int, default=0)
parser.add_argument("--missing", "-m", action="store_true", default=False)
parser.add_argument("--to_sqlite", "-s", type=str, default="")
parser.add_argument("--dump_stats", "-d", action="store_true", default=False)
parser.add_argument("--plot_stats", "-p", action="store_true", default=False)
args = parser.parse_args().__dict__

data_dir = args["path"]
file_range = range(int(args["begin_seed"]), int(args["end_seed"]) + 1)
stat_features = (
    "seed",
    "severity",
    "infectivity",
    "fatality",
    "birth_rate",
    "cure_threshold",
    "cure_started_day",
    "eradicated_day",
    "total_inf",
    "total_dead",
)

if args["missing"]:

    missing_files = []

    print(f"Files missing: ", end="")
    for f in file_range:
        if f"{f}.json" not in listdir(data_dir):
            print(f, end=", ")
    print("")

if args["to_sqlite"]:

    conn = sqlite3.connect(args["to_sqlite"])
    conn.execute("""
        CREATE TABLE STATS(
            seed INTEGER PRIMARY KEY,
            severity REAL NOT NULL,
            infectivity REAL NOT NULL,
            fatality REAL NOT NULL,
            birth_rate REAL NOT NULL,
            cure_threshold INTEGER NOT NULL,
            cure_started_day INTEGER NOT NULL,
            eradicated_day INTEGER NOT NULL,
            total_inf INTEGER NOT NULL,
            total_dead INTEGER NOT NULL
        )
    """)
    conn.commit()

    db = []
    row = []
    for seed in file_range:
        try:
            with open(path.join(data_dir, f"{seed}.json")) as data_file:
                data = json.load(data_file)
                row.append(str(seed))
                for feature in stat_features[1:]:
                    row.append(str(data[feature]))
                db.append(row)
                row = []
        except FileNotFoundError:
            print(f"{seed}.json missing")

    values = ",\n".join(f"({','.join(i)})" for i in db)
    print(f"""
        INSERT INTO STATS ({','.join(stat_features)}) VALUES {values};
        """)

    conn.execute(f"""
        INSERT INTO STATS ({','.join(stat_features)}) VALUES {values};
        """)
    conn.commit()

    conn.close()


if args["dump_stats"]:

    conn = sqlite3.connect(data_dir)

    AVG_QUERY = "SELECT AVG({0}) FROM STATS"
    MED_QUERY = """
    SELECT AVG({0})
    FROM (SELECT {0}
          FROM STATS
          ORDER BY {0}
          LIMIT 2 - (SELECT COUNT(*) FROM STATS) % 2    -- odd 1, even 2
          OFFSET (SELECT (COUNT(*) - 1) / 2
                  FROM STATS))
    """
    MAX_QUERY = "SELECT seed, MAX({0}) FROM STATS"
    MIN_QUERY = "SELECT seed, MIN({0}) FROM STATS"

    for feature in stat_features[1:]:
        print("---------------------------------------")
        print(feature)
        print("mean:", conn.execute(AVG_QUERY.format(feature)).fetchone()[0])
        print("median:", conn.execute(MED_QUERY.format(feature)).fetchone()[0])
        print("min:", conn.execute(MIN_QUERY.format(feature)).fetchone())
        print("max:", conn.execute(MAX_QUERY.format(feature)).fetchone())
        print("---------------------------------------")

    conn.close()

if args["plot_stats"]:

    import plotly
    from plotly.subplots import make_subplots

    conn = sqlite3.connect(data_dir)

    _text = [
        f"Seed: {seed}<br>" +
        f"Severity: {severity}<br>" +
        f"Infectivity: {infectivity}<br>" +
        f"Fatality: {fatality}<br>" +
        f"Birth rate: {birth_rate}<br>" +
        f"Cure threshold: {cure_threshold}<br>" +
        f"Cure Started Day: {cure_started_day}<br>"
        f"Days: {eradicated_day}<br>" +
        f"Total infected: {total_inf}<br>" +
        f"Total dead: {total_dead}<br>"
        for seed, severity, infectivity, fatality, birth_rate, cure_threshold, cure_started_day,
        eradicated_day, total_inf, total_dead, in conn.execute("SELECT * FROM STATS")
    ]

    fig = make_subplots(
        rows=1, cols=2,
        column_widths=[0.75, 0.25],
        shared_yaxes=True, horizontal_spacing=0.02
    )
    fig.add_trace(
        plotly.graph_objs.Scatter(
            x=[x[0] for x in conn.execute("SELECT infectivity FROM STATS")],
            y=[x[0] for x in conn.execute("SELECT total_inf FROM STATS")],
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
            y=[x[0] for x in conn.execute("SELECT total_inf FROM STATS")],
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

    conn.close()
