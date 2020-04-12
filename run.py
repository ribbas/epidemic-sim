#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os
from random import SystemRandom
from string import ascii_uppercase, digits
import sys

import sst

BASE_PATH = os.getcwd()
OUTPUT = True
CLOCK = "1Hz"
LINK_DELAY = "1ps"


def get_rand_tmp():
    return "/tmp/" + ''.join(
        SystemRandom().choice(ascii_uppercase + digits) for _ in range(16)
    )


# Main SST component
###############################################################################
for seed in range(int(sys.argv[-2]), int(sys.argv[-1]) + 1):

    seed = str(seed)

    epidemic_main = sst.Component(
        "Epidemic Simulation Driver " + seed, "epidemic.epidemic")
    epidemic_main.addParams({
        "SEED": int(seed),
        "OUTPUT": OUTPUT
    })

    # SystemC components
    ###############################################################################
    # Multiplicative inverse components
    mul_inv_sev_comp = sst.Component(
        "Severity Multiplicative Inverse (SystemC) " + seed, "epidemic.mul_inv")
    mul_inv_sev_comp.addParams({
        "OUTPUT": OUTPUT,
        "clock": CLOCK,
        "proc": os.path.join(BASE_PATH, "mul_inv.o"),
        "ipc_port": get_rand_tmp(),
    })

    mul_inv_inf_comp = sst.Component(
        "Infectivity Multiplicative Inverse (SystemC) " + seed, "epidemic.mul_inv")
    mul_inv_inf_comp.addParams({
        "OUTPUT": OUTPUT,
        "clock": CLOCK,
        "proc": os.path.join(BASE_PATH, "mul_inv.o"),
        "ipc_port": get_rand_tmp(),
    })

    mul_inv_fat_comp = sst.Component(
        "Fatality Multiplicative Inverse (SystemC) " + seed, "epidemic.mul_inv")
    mul_inv_fat_comp.addParams({
        "OUTPUT": OUTPUT,
        "clock": CLOCK,
        "proc": os.path.join(BASE_PATH, "mul_inv.o"),
        "ipc_port": get_rand_tmp(),
    })

    mul_inv_br_comp = sst.Component(
        "Birth Rate Multiplicative Inverse (SystemC) " + seed, "epidemic.mul_inv")
    mul_inv_br_comp.addParams({
        "OUTPUT": OUTPUT,
        "clock": CLOCK,
        "proc": os.path.join(BASE_PATH, "mul_inv.o"),
        "ipc_port": get_rand_tmp(),
    })

    mul_inv_rsrch_comp = sst.Component(
        "Research Multiplicative Inverse (SystemC) " + seed, "epidemic.mul_inv")
    mul_inv_rsrch_comp.addParams({
        "OUTPUT": OUTPUT,
        "clock": CLOCK,
        "proc": os.path.join(BASE_PATH, "mul_inv.o"),
        "ipc_port": get_rand_tmp(),
    })

    # Floor components
    floor_cure_thresh_comp = sst.Component(
        "Floor for Cure Threshold (SystemC) " + seed, "epidemic.sc_floor")
    floor_cure_thresh_comp.addParams({
        "OUTPUT": OUTPUT,
        "clock": CLOCK,
        "proc": os.path.join(BASE_PATH, "sc_floor.o"),
        "ipc_port": get_rand_tmp(),
    })

    floor_pop_inf_comp = sst.Component(
        "Floor for Infected Population (SystemC) " + seed, "epidemic.sc_floor")
    floor_pop_inf_comp.addParams({
        "OUTPUT": OUTPUT,
        "clock": CLOCK,
        "proc": os.path.join(BASE_PATH, "sc_floor.o"),
        "ipc_port": get_rand_tmp(),
    })

    floor_pop_dead_comp = sst.Component(
        "Floor for Dead Population (SystemC) " + seed, "epidemic.sc_floor")
    floor_pop_dead_comp.addParams({
        "OUTPUT": OUTPUT,
        "clock": CLOCK,
        "proc": os.path.join(BASE_PATH, "sc_floor.o"),
        "ipc_port": get_rand_tmp(),
    })

    # Multiplication components
    mul_pop_inf_comp = sst.Component(
        "Population Infected Multiplication (SystemC) " + seed, "epidemic.sc_mul")
    mul_pop_inf_comp.addParams({
        "OUTPUT": OUTPUT,
        "clock": CLOCK,
        "proc": os.path.join(BASE_PATH, "sc_mul.o"),
        "ipc_port": get_rand_tmp(),
    })

    mul_pop_dead_comp = sst.Component(
        "Population Dead Multiplication (SystemC) " + seed, "epidemic.sc_mul")
    mul_pop_dead_comp.addParams({
        "OUTPUT": OUTPUT,
        "clock": CLOCK,
        "proc": os.path.join(BASE_PATH, "sc_mul.o"),
        "ipc_port": get_rand_tmp(),
    })

    # Minimum float components
    minf_fat_comp = sst.Component(
        "Minimum Float Fatality (SystemC) " + seed, "epidemic.minf")
    minf_fat_comp.addParams({
        "OUTPUT": OUTPUT,
        "clock": CLOCK,
        "proc": os.path.join(BASE_PATH, "minf.o"),
        "ipc_port": get_rand_tmp(),
    })

    minf_inf_comp = sst.Component(
        "Minimum Float Infectivity (SystemC) " + seed, "epidemic.minf")
    minf_inf_comp.addParams({
        "OUTPUT": OUTPUT,
        "clock": CLOCK,
        "proc": os.path.join(BASE_PATH, "minf.o"),
        "ipc_port": get_rand_tmp(),
    })

    # Verilog components
    ###############################################################################
    _proc = []
    with open("config-cmd.json") as cmd_file:
        data = json.load(cmd_file)
    for k, v in data.items():
        if k != "FILE":
            os.environ[k] = v
        else:
            _proc = v

    flash_mem_comp = sst.Component(
        "Memory (Verilog) " + seed, "epidemic.flash_mem")
    flash_mem_comp.addParams({
        "OUTPUT": OUTPUT,
        "clock": CLOCK,
        "proc": _proc,
        "ipc_port": get_rand_tmp(),
    })

    # PyRTL components
    ###############################################################################
    mutation_comp = sst.Component(
        "Gene Mutation (PyRTL) " + seed, "epidemic.mutation")
    mutation_comp.addParams({
        "OUTPUT": OUTPUT,
        "clock": CLOCK,
        "proc": os.path.join(BASE_PATH, "../pyrtl/blackboxes/mutation_driver.py"),
        "ipc_port": get_rand_tmp(),
    })

    def connect_comps(comp, main_comp, comp_name, main_comp_name, seed):
        sst.Link(main_comp_name + "_din" + seed).connect(
            (comp, comp_name + "_din", LINK_DELAY),
            (main_comp, main_comp_name + "_din", LINK_DELAY)
        )
        sst.Link(main_comp_name + "_dout" + seed).connect(
            (comp, comp_name + "_dout", LINK_DELAY),
            (main_comp, main_comp_name + "_dout", LINK_DELAY)
        )

    # connect the subcomponents
    connect_comps(mul_inv_sev_comp, epidemic_main, "mul_inv", "mul_inv_sev", seed)
    connect_comps(mul_inv_inf_comp, epidemic_main, "mul_inv", "mul_inv_inf", seed)
    connect_comps(mul_inv_fat_comp, epidemic_main, "mul_inv", "mul_inv_fat", seed)
    connect_comps(mul_inv_br_comp, epidemic_main, "mul_inv", "mul_inv_br", seed)
    connect_comps(mul_inv_rsrch_comp, epidemic_main, "mul_inv", "mul_inv_rsrch", seed)

    connect_comps(minf_fat_comp, epidemic_main, "minf", "min_fat", seed)
    connect_comps(minf_inf_comp, epidemic_main, "minf", "min_inf", seed)

    connect_comps(floor_cure_thresh_comp, epidemic_main, "sc_floor", "floor_cure_thresh", seed)
    connect_comps(floor_pop_inf_comp, epidemic_main, "sc_floor", "floor_pop_inf", seed)
    connect_comps(floor_pop_dead_comp, epidemic_main, "sc_floor", "floor_pop_dead", seed)

    connect_comps(mul_pop_inf_comp, epidemic_main, "sc_mul", "mul_pop_inf", seed)
    connect_comps(mul_pop_dead_comp, epidemic_main, "sc_mul", "mul_pop_dead", seed)

    connect_comps(flash_mem_comp, epidemic_main, "flash_mem", "flash_mem", seed)

    connect_comps(mutation_comp, epidemic_main, "mutation", "mutation", seed)
