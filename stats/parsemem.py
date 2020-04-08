#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import json
import sys

if __name__ == "__main__":

    stats = {
        "factor": None,
        "severity": None,
        "infectivity": None,
        "fatality": None,
        "birth_rate": None,
        "cure_threshold": None,
        "cure_started_day": None,
        "cure_started_date": None,
        "cure_found_day": None,
        "cure_found_date": None,
        "eradicated_day": None,
        "eradicated_date": None,
        "total_inf": None,
        "total_dead": None,
        "plot_data": {
            "date": [],
            "inf_total": [],
            "dead_total": [],
            "cure": []
        }
    }

    with open(sys.argv[1]) as mem_dump_file:

        addr = []
        data = []

        def split_line(line):
            _addr, _data = line.split()
            addr.append(_addr)
            data.append(_data)

        [split_line(line) for line in mem_dump_file]

        _stats = data[-7:-1]
        for stats_line in range(6):
            _stats[stats_line] = str(int(_stats[stats_line], 2)).zfill(8)
            if not stats_line:
                stats["factor"] = int(_stats[stats_line])
            elif stats_line == 1:
                stats["severity"] = float("0." + _stats[stats_line][1:])
            elif stats_line == 2:
                stats["infectivity"] = float("0." + _stats[stats_line][1:])
            elif stats_line == 3:
                stats["fatality"] = float("0." + _stats[stats_line][1:])
            elif stats_line == 4:
                stats["birth_rate"] = float("0." + _stats[stats_line][1:])
            elif stats_line == 5:
                stats["cure_threshold"] = int(_stats[stats_line])

        total_inf = 0
        total_dead = 0
        today = datetime.date.today()

        for _addr, _data in zip(addr[:-7], data[:-7]):

            if "x" in _data:
                stats["eradicated_day"] = int(_addr)
                stats["eradicated_date"] = (
                    today + datetime.timedelta(stats["eradicated_day"])).isoformat()
                break

            _data = str(int(_data, 2)).zfill(8)
            pop_dead, pop_inf, cure = int(_data[0:3]), int(_data[3:6]), int(_data[6:8])

            if not stats["cure_started_day"] and cure == 1:
                stats["cure_started_day"] = int(_addr)
                stats["cure_started_date"] = (
                    today + datetime.timedelta(stats["cure_started_day"])).isoformat()
            elif not stats["cure_found_day"] and not cure and stats["cure_started_day"]:
                stats["cure_found_day"] = int(_addr)
                stats["cure_found_date"] = (
                    today + datetime.timedelta(stats["cure_found_day"])).isoformat()

            total_inf += pop_inf * stats["factor"]
            total_dead += pop_dead * stats["factor"]

            _date = today + datetime.timedelta(int(_addr))
            stats["plot_data"]["date"].append(_date.isoformat())
            stats["plot_data"]["inf_total"].append(total_inf)
            stats["plot_data"]["dead_total"].append(total_dead)
            stats["plot_data"]["cure"].append(cure)

        stats["total_inf"] = total_inf
        stats["total_dead"] = total_dead

        print(f"Cure started on {stats['cure_started_date']}")
        print(f"Cure found on {stats['cure_found_date']}")
        print(f"Disease eradicated on {stats['eradicated_date']}")
        with open(f"data/{sys.argv[2]}.json", "w") as stats_dump_file:
            json.dump(stats, stats_dump_file)
