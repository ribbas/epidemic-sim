#!/usr/bin/env python
# -*- coding: utf-8 -*-

from argparse import ArgumentParser
import json
from os import listdir, path
import sqlite3

parser = ArgumentParser()
parser.add_argument("path", type=str)
parser.add_argument("end_seed", type=int, default=0)
parser.add_argument("--start_seed", "-s", type=int, default=0)
parser.add_argument("--missing", "-m", action="store_true", default=False)
parser.add_argument("--db", "-d", type=str, default="")
args = parser.parse_args().__dict__

data_dir = args["path"]
file_range = range(int(args["start_seed"]), int(args["end_seed"]) + 1)

if args["missing"]:

    missing_files = []

    print(f"Files missing: ", end="")
    with open("stats/missing.txt", "w") as missing_file:
        for f in file_range:
            if f"{f}.json" not in listdir(data_dir):
                print(f, end=", ")
                missing_file.write(f"{f}\n")
    print("")

if args["db"]:

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

    conn = sqlite3.connect(args["db"])
    conn.execute("""
        CREATE TABLE IF NOT EXISTS STATS(
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
    db1 = f"""
    INSERT INTO STATS ({','.join(stat_features)})
    VALUES
"""
    row = []
    for seed in file_range:
        try:
            with open(path.join(data_dir, f"{seed}.json")) as data_file:
                data = json.load(data_file)
                row.append(str(seed))
                for feature in stat_features[1:]:
                    row.append(str(data[feature]))
                db.append(row)
                db1 += f"({','.join(row)}),\n"
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
