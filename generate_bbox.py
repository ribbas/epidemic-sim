#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from boilerplate import Chisel, PyRTL, SystemC

if __name__ == "__main__":

    ARGS = {
        "lib": "epidemic",
        "module_dir": "../",
        "ipc": "sock",
        "lib_dir": "../../../../sit/",
    }

    if sys.argv[-1] == "systemc":

        minf = SystemC(
            **ARGS,
            module="minf",
        )
        minf.set_ports((
            ("input", "operand1", "<float>", 12),
            ("input", "operand2", "<float>", 5),
            ("output", "data_out", "<float>", 12),
        ))
        minf.fixed_width_float_output(9)
        minf.disable_runtime_warnings(["SC_ID_NO_SC_START_ACTIVITY_"])
        minf.generate_bbox()

        sc_mul = SystemC(
            **ARGS,
            module="sc_mul",
        )
        sc_mul.set_ports((
            ("input", "operandi", "<sc_uint<11>>"),
            ("input", "operandf", "<float>", 12),
            ("output", "data_out", "<float>", 12),
        ))
        sc_mul.fixed_width_float_output(8)
        sc_mul.disable_runtime_warnings(["SC_ID_NO_SC_START_ACTIVITY_"])
        sc_mul.generate_bbox()

        mul_inv = SystemC(
            **ARGS,
            module="mul_inv",
        )
        mul_inv.set_ports((
            ("input", "operand", "<sc_uint<10>>"),
            ("output", "data_out", "<float>", 12),
        ))
        mul_inv.fixed_width_float_output(9)
        mul_inv.disable_runtime_warnings(["SC_ID_NO_SC_START_ACTIVITY_"])
        mul_inv.generate_bbox()

        sc_floor = SystemC(
            **ARGS,
            module="sc_floor",
        )
        sc_floor.set_ports((
            ("input", "operand", "<float>", 12),
            ("output", "data_out", "<sc_uint<25>>"),
        ))
        sc_floor.disable_runtime_warnings(["SC_ID_NO_SC_START_ACTIVITY_"])
        sc_floor.generate_bbox()

    elif sys.argv[-1] == "pyrtl":
        mutation = PyRTL(
            **ARGS,
            module="mutation",
        )
        mutation.set_ports((
            ("input", "chance", "3"),
            ("input", "gene", "3"),
            ("output", "out", "2"),
        ))
        mutation.generate_bbox()

    elif sys.argv[-1] == "chisel":

        flash_mem = Chisel(
            **ARGS,
            module="flash_mem",
        )
        flash_mem.set_ports((
            ("input", "address", "10"),
            ("input", "cs", "1"),
            ("input", "we", "1"),
            ("input", "oe", "1"),
            ("input", "data_in", "25"),
            ("output", "data_out", "25"),
        ))
        flash_mem.generate_bbox()
