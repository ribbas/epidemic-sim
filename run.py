#!/usr/bin/env python
# -*- coding: utf-8 -*-

from random import SystemRandom
from string import ascii_uppercase, digits
import os

import sst

BASE_PATH = os.getcwd()

CLOCK = "1Hz"

LINK_DELAY = "1ps"


def get_rand_tmp():
    return "/tmp/" + ''.join(
        SystemRandom().choice(ascii_uppercase + digits) for _ in range(8)
    )


# Main SST component
###############################################################################
plague_main = sst.Component(
    "Plague Simulation Driver", "plague.plague")
plague_main.addParams({
    "CLOCK": CLOCK,
    "SEED0": "15462",
})

# SystemC components
###############################################################################
# RNG components
rng_limit_comp = sst.Component(
    "Random Limit Component (SystemC)", "plague.rng")
rng_limit_comp.addParams({
    "clock": CLOCK,
    "proc": os.path.join(BASE_PATH, "rng.o"),
    "ipc_port": get_rand_tmp(),
})

rng_pop_inf_comp = sst.Component(
    "Infected Population RNG Component (SystemC)", "plague.rng")
rng_pop_inf_comp.addParams({
    "clock": CLOCK,
    "proc": os.path.join(BASE_PATH, "rng.o"),
    "ipc_port": get_rand_tmp(),
})

rng_mut_comp = sst.Component(
    "Mutation RNG Component (SystemC)", "plague.rng")
rng_mut_comp.addParams({
    "clock": CLOCK,
    "proc": os.path.join(BASE_PATH, "rng.o"),
    "ipc_port": get_rand_tmp(),
})

# Random Float components
randf_sev_comp = sst.Component(
    "Severity Component (SystemC)", "plague.randf")
randf_sev_comp.addParams({
    "clock": CLOCK,
    "proc": os.path.join(BASE_PATH, "randf.o"),
    "ipc_port": get_rand_tmp(),
})

randf_inf_comp = sst.Component(
    "Infectivity Component (SystemC)", "plague.randf")
randf_inf_comp.addParams({
    "clock": CLOCK,
    "proc": os.path.join(BASE_PATH, "randf.o"),
    "ipc_port": get_rand_tmp(),
})

randf_fat_comp = sst.Component(
    "Fatality Component (SystemC)", "plague.randf")
randf_fat_comp.addParams({
    "clock": CLOCK,
    "proc": os.path.join(BASE_PATH, "randf.o"),
    "ipc_port": get_rand_tmp(),
})

randf_br_comp = sst.Component(
    "Birth Rate Component (SystemC)", "plague.randf")
randf_br_comp.addParams({
    "clock": CLOCK,
    "proc": os.path.join(BASE_PATH, "randf.o"),
    "ipc_port": get_rand_tmp(),
})

randf_rsrch_comp = sst.Component(
    "Research Component (SystemC)", "plague.randf")
randf_rsrch_comp.addParams({
    "clock": CLOCK,
    "proc": os.path.join(BASE_PATH, "randf.o"),
    "ipc_port": get_rand_tmp(),
})

# Floor components
floor_cure_thresh_comp = sst.Component(
    "Floor Component for Cure Threshold (SystemC)", "plague.sc_floor")
floor_cure_thresh_comp.addParams({
    "clock": CLOCK,
    "proc": os.path.join(BASE_PATH, "sc_floor.o"),
    "ipc_port": get_rand_tmp(),
})

floor_pop_inf_comp = sst.Component(
    "Floor Component for Infected Population (SystemC)", "plague.sc_floor")
floor_pop_inf_comp.addParams({
    "clock": CLOCK,
    "proc": os.path.join(BASE_PATH, "sc_floor.o"),
    "ipc_port": get_rand_tmp(),
})

floor_pop_dead_comp = sst.Component(
    "Floor Component for Dead Population (SystemC)", "plague.sc_floor")
floor_pop_dead_comp.addParams({
    "clock": CLOCK,
    "proc": os.path.join(BASE_PATH, "sc_floor.o"),
    "ipc_port": get_rand_tmp(),
})

# mulonential components
mul_pop_inf_comp = sst.Component(
    "Population Infected Multiplication Component (SystemC)", "plague.sc_mul")
mul_pop_inf_comp.addParams({
    "clock": CLOCK,
    "proc": os.path.join(BASE_PATH, "sc_mul.o"),
    "ipc_port": get_rand_tmp(),
})

mul_pop_dead_comp = sst.Component(
    "Population Dead Multiplication Component (SystemC)", "plague.sc_mul")
mul_pop_dead_comp.addParams({
    "clock": CLOCK,
    "proc": os.path.join(BASE_PATH, "sc_mul.o"),
    "ipc_port": get_rand_tmp(),
})

# Minimum float components
minf_fat_comp = sst.Component(
    "Minimum Float Fatality Component (SystemC)", "plague.minf")
minf_fat_comp.addParams({
    "clock": CLOCK,
    "proc": os.path.join(BASE_PATH, "minf.o"),
    "ipc_port": get_rand_tmp(),
})

minf_inf_comp = sst.Component(
    "Minimum Float Infectivity Component (SystemC)", "plague.minf")
minf_inf_comp.addParams({
    "clock": CLOCK,
    "proc": os.path.join(BASE_PATH, "minf.o"),
    "ipc_port": get_rand_tmp(),
})

# Chisel components
###############################################################################
flash_mem_comp = sst.Component(
    "Memory Component (Chisel)", "plague.flash_mem")
flash_mem_comp.addParams({
    "clock": CLOCK,
    "proc": "test:runMain flash_mem.flash_memMain",
    "ipc_port": get_rand_tmp(),
})

# PyRTL components
###############################################################################
print(os.path.join(BASE_PATH, "../pyrtl/blackboxes/mutation_driver.py"))
mutation_comp = sst.Component(
    "Gene Mutation Component (PyRTL)", "plague.mutation")
mutation_comp.addParams({
    "clock": CLOCK,
    "proc": os.path.join(BASE_PATH, "../pyrtl/blackboxes/mutation_driver.py"),
    "ipc_port": get_rand_tmp(),
})


def connect_comps(comp, main_comp, comp_name, main_comp_name):
    sst.Link(main_comp_name + "_din").connect(
        (comp, comp_name + "_din", LINK_DELAY),
        (main_comp, main_comp_name + "_din", LINK_DELAY)
    )
    sst.Link(main_comp_name + "_dout").connect(
        (comp, comp_name + "_dout", LINK_DELAY),
        (main_comp, main_comp_name + "_dout", LINK_DELAY)
    )


# connect the subcomponents
connect_comps(rng_limit_comp, plague_main, "rng", "rng_limit")
connect_comps(rng_pop_inf_comp, plague_main, "rng", "rng_pop_inf")
connect_comps(rng_mut_comp, plague_main, "rng", "rng_mut")

connect_comps(randf_sev_comp, plague_main, "randf", "randf_sev")
connect_comps(randf_inf_comp, plague_main, "randf", "randf_inf")
connect_comps(randf_fat_comp, plague_main, "randf", "randf_fat")
connect_comps(randf_br_comp, plague_main, "randf", "randf_br")
connect_comps(randf_rsrch_comp, plague_main, "randf", "randf_rsrch")

connect_comps(minf_fat_comp, plague_main, "minf", "min_fat")
connect_comps(minf_inf_comp, plague_main, "minf", "min_inf")

connect_comps(floor_cure_thresh_comp, plague_main, "sc_floor", "floor_cure_thresh")
connect_comps(floor_pop_inf_comp, plague_main, "sc_floor", "floor_pop_inf")
connect_comps(floor_pop_dead_comp, plague_main, "sc_floor", "floor_pop_dead")

connect_comps(mul_pop_inf_comp, plague_main, "sc_mul", "mul_pop_inf")
connect_comps(mul_pop_dead_comp, plague_main, "sc_mul", "mul_pop_dead")

connect_comps(flash_mem_comp, plague_main, "flash_mem", "flash_mem")

connect_comps(mutation_comp, plague_main, "mutation", "mutation")
