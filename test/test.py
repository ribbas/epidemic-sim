#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
import random
from pprint import pprint

SEED = 1234
LIMIT = 10

POPULATION_TOTAL = 7721989320
POPULATION_TOTAL = 1000
POPULATION_INFECTED = 0
POPULATION_DEAD = 0

random.seed(SEED)
SEVERITY = 1 / random.randint(1, LIMIT)  # detection rate
LETHALITY = 1 / random.randint(1, LIMIT)  # rate of population decrease
INFECTIVITY = 1 / random.randint(1, LIMIT)  # rate of infection

# (LETHALITY * INFECTIVITY) + (SEVERITY * LETHALITY) + (SEVERITY * INFECTIVITY)
CURE = 0.0
CURE_THRESHOLD = math.ceil(SEVERITY / LIMIT * POPULATION_TOTAL)

pprint(globals())

while POPULATION_INFECTED <= CURE_THRESHOLD:
    POPULATION_INFECTED += math.ceil(POPULATION_TOTAL * INFECTIVITY)
    print(POPULATION_INFECTED, POPULATION_TOTAL)
