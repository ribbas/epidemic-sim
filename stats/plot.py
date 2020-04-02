#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import json
import math
import sys

import plotly
import plotly.graph_objs as go

if __name__ == "__main__":
    with open(sys.argv[-1]) as stats_dump_file:
        data = json.load(stats_dump_file)

        max_y_val = data["plot_data"]["inf_total"][-1] + \
            data["plot_data"]["inf_total"][int(data["eradicated_day"] / 4)]

        def gaussian_func(x, scale, shift):
            return scale * math.exp(-1 / 2 * math.pow((x - shift) / (shift / math.pi), 2))

        bell_curve = [
            gaussian_func(x, data["plot_data"]["inf_total"][-1], data["cure_found_day"])
            for x in range(data["eradicated_day"])
        ]
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=data["plot_data"]["date"], y=data["plot_data"]["inf_total"],
            name="population infected (actual)", fill="tozeroy",
            line={"color": "rgb(255,154,0)"},
        ))
        fig.add_trace(go.Scatter(
            x=data["plot_data"]["date"], y=bell_curve,
            name="population infected (predicted)",
            line={"color": "rgb(155, 89, 182)", "width": 4},
        ))
        fig.add_trace(go.Scatter(
            x=data["plot_data"]["date"], y=data["plot_data"]["dead_total"],
            name="population dead", fill="tozeroy",
            line={"color": "rgb(231, 76, 60)"},
        ))

        cure_started_date = datetime.datetime.strptime(data["cure_started_date"], "%Y-%m-%d")
        cure_started_date_val = data["plot_data"]["inf_total"][-1]
        fig.add_annotation(
            x=cure_started_date,
            y=max_y_val,
            text="Cure started"
        )
        fig.add_shape({
            "type": "line",
            "name": "cure started date",
            "x0": cure_started_date,
            "y0": 0,
            "x1": cure_started_date,
            "y1": max_y_val - 20000,
            "line": {"color": "rgb(97,212,179)"}
        })

        cure_found_date = datetime.datetime.strptime(data["cure_found_date"], "%Y-%m-%d")
        fig.add_shape({
            "type": "line",
            "name": "cure found date",
            "x0": cure_found_date,
            "y0": 0,
            "x1": cure_found_date,
            "y1": max_y_val - 20000,
            "line": {"color": "rgb(97,212,179)"}
        })
        fig.add_annotation(
            x=cure_found_date,
            y=max_y_val,
            text="Cure found"
        )

        eradicated_date = datetime.datetime.strptime(data["eradicated_date"], "%Y-%m-%d")
        fig.add_shape({
            "type": "line",
            "x0": eradicated_date,
            "y0": 0,
            "x1": eradicated_date,
            "y1": max_y_val - 20000,
            "line": {"color": "rgb(97,212,179)"}
        })
        fig.add_annotation(
            x=eradicated_date,
            y=max_y_val,
            text="Disease eradicated"
        )
        fig.update_annotations(
            dict(
                xref="x",
                yref="y",
                showarrow=True,
                arrowhead=7,
                ax=0,
                ay=-40,
                textangle=-90
            )
        )

        plotly.io.orca.config.executable = "/home/sabbir/Downloads/orca-1.3.1.AppImage"
        fig.write_image("docs/sample0.png", scale=5, width=1100, height=900)
        fig.show()
