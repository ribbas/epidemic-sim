#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
import random
import sys

SEED = int(sys.argv[-1])
random.seed(SEED)
LIMIT = random.randint(3, 1000)


def rand_float():
    return 1 / random.randint(2, LIMIT)


def mutations(lethality, infectivity, cure, research):
    MUTATED_GENE = random.randint(0, 8)
    if str(lethality)[-1] == str(MUTATED_GENE + 1):
        return abs(cure - research), infectivity
    elif str(lethality)[-1] == str(MUTATED_GENE):
        return cure, abs(infectivity - rand_float())
    else:
        return cure, infectivity


POPULATION_TOTAL = 7760000000
POPULATION_HEALTHY = POPULATION_TOTAL
POPULATION_INFECTED = 0
TOTAL_INFECTED = 0
POPULATION_DEAD = 0
TOTAL_DEAD = 0
POPULATION_AFFECTED = 0

BIRTH_RATE = rand_float()

SEVERITY = rand_float()  # rate of detection
LETHALITY = rand_float()  # rate of death
INFECTIVITY = rand_float()  # rate of infection

CURE = 0.00
CURE_THRESHOLD = math.ceil(POPULATION_TOTAL * SEVERITY * BIRTH_RATE)

TIME = 0

while POPULATION_HEALTHY > 0 and CURE < 100:

    INFECTIVITY = min(INFECTIVITY + rand_float(), 0.99)
    LETHALITY = min(LETHALITY + rand_float(), 0.99)
    RESEARCH = rand_float()
    if TOTAL_INFECTED > CURE_THRESHOLD:
        CURE += RESEARCH
        CURE, INFECTIVITY = mutations(LETHALITY, INFECTIVITY, CURE, RESEARCH)
    POPULATION_INFECTED = min(POPULATION_HEALTHY, math.ceil(
        random.randint(1, 100) * math.exp(INFECTIVITY)))
    TOTAL_INFECTED += POPULATION_INFECTED
    POPULATION_DEAD = math.ceil(POPULATION_INFECTED * LETHALITY)
    TOTAL_DEAD += POPULATION_DEAD
    POPULATION_HEALTHY = POPULATION_HEALTHY - POPULATION_DEAD - \
                         POPULATION_INFECTED + random.randint(1, 100) * math.ceil(math.exp(BIRTH_RATE))
    if POPULATION_HEALTHY < 1:
        POPULATION_HEALTHY += POPULATION_DEAD + POPULATION_INFECTED
        print("\033[91mHUMANITY ERADICATED\033[00m")
        break
    print(
        f"TIME: {TIME}, CURE: {CURE}, INFECTED: {POPULATION_INFECTED}, DEAD: {POPULATION_DEAD}, HEALTHY: {POPULATION_HEALTHY}")
    TIME += 1

print(f"SEED: {SEED}")
print(
    f"INFECTIVITY: {INFECTIVITY}, LETHALITY: {LETHALITY}, SEVERITY: {SEVERITY}, THRESHOLD: {CURE_THRESHOLD}")
print(f"INFECTED: {TOTAL_INFECTED} ({round(TOTAL_INFECTED / POPULATION_TOTAL * 100, 2)}%)")
print(f"DEAD: {TOTAL_DEAD} ({round(TOTAL_DEAD / POPULATION_TOTAL * 100, 2)}%)")
print(
    f"INFECTED BUT ALIVE: {TOTAL_INFECTED - TOTAL_DEAD} ({round((TOTAL_INFECTED - TOTAL_DEAD) / POPULATION_TOTAL * 100, 2)}%)")
print(
    f"ALIVE: {POPULATION_HEALTHY + (TOTAL_INFECTED - TOTAL_DEAD)} ({round((POPULATION_HEALTHY + (TOTAL_INFECTED - TOTAL_DEAD)) / POPULATION_TOTAL * 100, 2)}%)")
print(f"HEALTHY: {POPULATION_HEALTHY} ({round(POPULATION_HEALTHY / POPULATION_TOTAL * 100, 2)}%)")
