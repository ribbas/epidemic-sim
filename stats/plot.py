#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import json
import sys

import plotly.graph_objs as go

if __name__ == "__main__":
    with open(sys.argv[-1]) as stats_dump_file:
        data = json.load(stats_dump_file)

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=data["plot_data"]["date"], y=data["plot_data"]["inf_total"],
            name="population infected", fill="tozeroy",
            line={"color": "rgb(255,154,0)"}, mode="lines+markers"
        ))
        fig.add_trace(go.Scatter(
            x=data["plot_data"]["date"], y=data["plot_data"]["dead_total"],
            name="population dead", fill="tozeroy",
            line={"color": "rgb(255,0,0)"}, mode="lines+markers"
        ))
        fig.update_layout(barmode="stack")

        cure_started_date = datetime.datetime.strptime(data["cure_started_date"], "%Y-%m-%d")
        cure_started_date_val = data["plot_data"]["inf_total"][-1]
        fig.add_trace(go.Scatter(
            x=[cure_started_date + datetime.timedelta(80)],
            y=[cure_started_date_val],
            text=["Cure started"],
            mode="text",
        ))
        fig.add_shape({
            "type": "line",
            "x0": cure_started_date,
            "y0": 0,
            "x1": cure_started_date,
            "y1": cure_started_date_val,
            "line": {"color": "rgb(97,212,179)"}
        })
        fig.show()
