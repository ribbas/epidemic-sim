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
            line={"color": "rgb(255,154,0)"},
        ))
        fig.add_trace(go.Scatter(
            x=data["plot_data"]["date"], y=data["plot_data"]["dead_total"],
            name="population dead", fill="tozeroy",
            line={"color": "rgb(255,0,0)"},
        ))
        fig.update_layout(barmode="stack")

        max_y_val = data["plot_data"]["inf_total"][-1] + \
            data["plot_data"]["inf_total"][int(data["days"] / 4)]

        cure_started_date = datetime.datetime.strptime(data["cure_started_date"], "%Y-%m-%d")
        cure_started_date_val = data["plot_data"]["inf_total"][-1]
        fig.add_trace(go.Scatter(
            x=[cure_started_date],
            y=[max_y_val],
            name="cure started date",
            text=["Cure started"],
            mode="text",
        ))
        fig.add_shape({
            "type": "line",
            "name": "cure started date",
            "x0": cure_started_date,
            "y0": 0,
            "x1": cure_started_date,
            "y1": max_y_val - 10000,
            "line": {"color": "rgb(97,212,179)"}
        })

        cure_found_date = datetime.datetime.strptime(data["cure_found_date"], "%Y-%m-%d")
        fig.add_trace(go.Scatter(
            x=[cure_found_date],
            y=[max_y_val],
            name="cure found date",
            text=["Cure found"],
            mode="text",
        ))
        fig.add_shape({
            "type": "line",
            "name": "cure found date",
            "x0": cure_found_date,
            "y0": 0,
            "x1": cure_found_date,
            "y1": max_y_val - 10000,
            "line": {"color": "rgb(97,212,179)"}
        })

        eradicated_date = datetime.datetime.strptime(data["eradicated_date"], "%Y-%m-%d")
        fig.add_trace(go.Scatter(
            x=[eradicated_date],
            y=[max_y_val],
            name="disease eradicated date",
            text=["Disease eradicated"],
            mode="text",
        ))
        fig.add_shape({
            "type": "line",
            "name": "disease eradicated date",
            "x0": eradicated_date,
            "y0": 0,
            "x1": eradicated_date,
            "y1": max_y_val - 10000,
            "line": {"color": "rgb(97,212,179)"}
        })

        fig.show()
