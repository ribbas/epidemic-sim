#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from os import listdir, path
import statistics
import sys

file_range = range(0, 490)
data_dir = sys.argv[1]
PENDING_FILES = []

for f in file_range:
    if f"{f}.json" not in listdir(data_dir):
        PENDING_FILES.append(str(f))

with open("stats/pending.txt", "w") as pending_file:
    print("\n".join(PENDING_FILES))
    pending_file.write("\n".join(PENDING_FILES))
