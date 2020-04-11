import math
import random
import sys
TIME = 0
IS_ERADICTED = False
while not IS_ERADICTED:
    if TIME == 0:
        random.seed(int(sys.argv[-1]))
        LIMIT = random.randint(100, 1023)
        POPULATION_INFECTED = 0
        TOTAL_INFECTED = 0
        TOTAL_DEAD = 0
        POPULATION_DEAD = 0
        BIRTH_RATE = 1 / random.randint(100, LIMIT)
        SEVERITY = 1 / random.randint(100, LIMIT)
        FATALITY = 1 / random.randint(100, LIMIT)
        INFECTIVITY = 1 / random.randint(100, LIMIT)
        CURE_THRESHOLD = math.floor(7760000000 * SEVERITY * BIRTH_RATE) / LIMIT
        CURE = 0.00
        print("| DAY |  CURE  | INF | DEAD |\n|-----|--------|-----|------|")
    else:
        INFECTIVITY = min(0.50, INFECTIVITY + (1 / random.randint(100, LIMIT)))
        FATALITY = min(0.25, FATALITY + (1 / random.randint(100, LIMIT)))
        if TOTAL_INFECTED > CURE_THRESHOLD:
            RESEARCH = 1 / random.randint(2, 10)
            CURE += RESEARCH
            MUTATED_GENE = random.randint(0, 8)
            if str(FATALITY)[-1] == str(MUTATED_GENE + 1):
                CURE = abs(CURE - RESEARCH)
            elif str(FATALITY)[-1] == str(MUTATED_GENE):
                INFECTIVITY = abs(INFECTIVITY - RESEARCH)
        BATCH_INFECTED = random.randint(TIME, 1998) if CURE < 100.00 else random.randint(0, 100)
        IS_ERADICTED = not BATCH_INFECTED
        POPULATION_INFECTED = math.floor(BATCH_INFECTED * INFECTIVITY)
        POPULATION_DEAD = math.floor(POPULATION_INFECTED * FATALITY)
        TOTAL_INFECTED += POPULATION_INFECTED
        TOTAL_DEAD += POPULATION_DEAD
    print(f"|{TIME:4} | {CURE:6.2f} | {POPULATION_INFECTED:3} | {POPULATION_DEAD:4} |")
    TIME += 1
