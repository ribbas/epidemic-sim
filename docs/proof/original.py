import math
import random
import sys

POPULATION_TOTAL = 7760000000
CURE = 0.00
TIME = 0

while CURE < 100.00:

    if TIME == 0:

        random.seed(int(sys.argv[-1]))
        LIMIT = random.randint(100, 1023)

        POPULATION_INFECTED = 0
        TOTAL_INFECTED = 0
        TOTAL_DEAD = 0
        POPULATION_DEAD = 0
        BIRTH_RATE = 1 / random.randint(100, LIMIT)
        SEVERITY = 1 / random.randint(100, LIMIT)  # rate of detection
        FATALITY = 1 / random.randint(100, LIMIT)  # rate of death
        INFECTIVITY = 1 / random.randint(100, LIMIT)  # rate of infection
        CURE_THRESHOLD = math.floor(POPULATION_TOTAL * SEVERITY * BIRTH_RATE) / LIMIT

    else:

        INFECTIVITY = min(0.50, INFECTIVITY + (1 / random.randint(100, LIMIT)))
        FATALITY = min(0.25, FATALITY + (1 / random.randint(100, LIMIT)))

        if TOTAL_INFECTED > CURE_THRESHOLD:

            RESEARCH = 1 / random.randint(2, 10)
            CURE += RESEARCH

            MUTATED_GENE = random.randint(0, 8)
            MUTATED_GENE1 = MUTATED_GENE + 1

            if str(FATALITY)[-1] == str(MUTATED_GENE1):
                CURE = abs(CURE - RESEARCH)

            elif str(FATALITY)[-1] == str(MUTATED_GENE):
                INFECTIVITY = abs(INFECTIVITY - RESEARCH)

        BATCH_INFECTED = random.randint(TIME + 1197, 1198)
        POPULATION_INFECTED = math.floor(BATCH_INFECTED * INFECTIVITY)
        POPULATION_DEAD = math.floor(POPULATION_INFECTED * FATALITY)

        TOTAL_INFECTED += POPULATION_INFECTED
        TOTAL_DEAD += POPULATION_DEAD

    print(f"TIME: {TIME}, CURE: {CURE}, INFECTED: {POPULATION_INFECTED}, DEAD: {POPULATION_DEAD}")
    TIME += 1
