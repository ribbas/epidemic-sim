#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
import random
import sys

POPULATION_TOTAL = 7760000000
# POPULATION_HEALTHY = POPULATION_TOTAL
CURE = 0.00
TIME = 0

while CURE < 100:

    if TIME == 0:

        SEED = int(sys.argv[-1])
        random.seed(SEED)
        LIMIT = random.randint(100, 1023)

        POPULATION_INFECTED = 0
        TOTAL_INFECTED = 0
        POPULATION_DEAD = 0
        TOTAL_DEAD = 0
        POPULATION_AFFECTED = 0

        BIRTH_RATE = random.randint(100, LIMIT)
        BIRTH_RATE = 1 / BIRTH_RATE

        SEVERITY = random.randint(100, LIMIT)
        SEVERITY = 1 / SEVERITY  # rate of detection

        FATALITY = random.randint(100, LIMIT)
        FATALITY = 1 / FATALITY  # rate of death

        INFECTIVITY = random.randint(100, LIMIT)
        INFECTIVITY = 1 / INFECTIVITY  # rate of infection

        CURE_THRESHOLD = POPULATION_TOTAL * SEVERITY
        CURE_THRESHOLD = CURE_THRESHOLD * BIRTH_RATE
        CURE_THRESHOLD = math.floor(CURE_THRESHOLD)

    else:

        _INFECTIVITY = random.randint(100, LIMIT)
        _INFECTIVITY = 1 / _INFECTIVITY
        INFECTIVITY = INFECTIVITY + _INFECTIVITY
        INFECTIVITY = min(INFECTIVITY, 0.25)

        _FATALITY = random.randint(100, LIMIT)
        _FATALITY = 1 / _FATALITY
        FATALITY = FATALITY + _FATALITY
        FATALITY = min(FATALITY, 0.25)

        if TOTAL_INFECTED > CURE_THRESHOLD:

            RESEARCH = random.randint(2, 100)
            RESEARCH = 1 / RESEARCH
            CURE = CURE + RESEARCH

            MUTATED_GENE = random.randint(0, 8)
            MUTATED_GENE1 = MUTATED_GENE + 1

            if str(FATALITY)[-1] == str(MUTATED_GENE1):
                CURE = CURE - RESEARCH
                CURE = abs(CURE)

            elif str(FATALITY)[-1] == str(MUTATED_GENE):
                INFECTIVITY = INFECTIVITY - RESEARCH
                INFECTIVITY = abs(INFECTIVITY)

        BATCH_INFECTED = random.randint(1, 10)

        POPULATION_INFECTED = BATCH_INFECTED * INFECTIVITY
        POPULATION_INFECTED = math.floor(POPULATION_INFECTED)

        POPULATION_DEAD = POPULATION_INFECTED * FATALITY
        POPULATION_DEAD = math.floor(POPULATION_DEAD)

        TOTAL_INFECTED = TOTAL_INFECTED + POPULATION_INFECTED
        TOTAL_DEAD = TOTAL_DEAD + POPULATION_DEAD

    print(f"TIME: {TIME}, CURE: {CURE}, INFECTED: {POPULATION_INFECTED}, DEAD: {POPULATION_DEAD}")
    TIME += 1

print(f"SEED: {SEED}")
print(
    f"INFECTIVITY: {INFECTIVITY}, FATALITY: {FATALITY}, SEVERITY: {SEVERITY}, THRESHOLD: {CURE_THRESHOLD}")
print(f"INFECTED: {TOTAL_INFECTED} ({round(TOTAL_INFECTED / POPULATION_TOTAL * 100, 2)}%)")
print(f"DEAD: {TOTAL_DEAD} ({round(TOTAL_DEAD / POPULATION_TOTAL * 100, 2)}%)")
print(
    f"INFECTED BUT ALIVE: {TOTAL_INFECTED - TOTAL_DEAD} ({round((TOTAL_INFECTED - TOTAL_DEAD) / POPULATION_TOTAL * 100, 2)}%)")
# print(f"ALIVE: {POPULATION_HEALTHY + (TOTAL_INFECTED - TOTAL_DEAD)} ({round((POPULATION_HEALTHY + (TOTAL_INFECTED - TOTAL_DEAD)) / POPULATION_TOTAL * 100, 2)}%)")
# print(f"HEALTHY: {POPULATION_HEALTHY} ({round(POPULATION_HEALTHY / POPULATION_TOTAL * 100, 2)}%)")
