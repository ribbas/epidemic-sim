# epidemic-sim

A disease spread simulator using SST with SystemC, PyRTL and Verilog models.

## Installation

### Requirements
This simulator requires the [SST Interoperability Toolkit](https://github.com/sabbirahm3d/SIT) to generate the black box interfaces that establish communication between the frameworks.

|Requirement|Version|
|-----------|-------|
|SIT|0.9.4|
|SystemC|2.3.3|
|PyRTL|0.8.7|
|cocotb|1.3.1|
|Icarus Verilog|10.1|


The provided Makefile can be used to generate the black box interfaces, compile and run the simulation.

- `make generate`: generate the SystemC, PyRTL and Verilog black box interfaces
- `make install`: compile all the simulation files
- `make run SEED1=N SEED2=M`: run simulations with the RNG seeds `N` to `M`
- `make stats SEED1=N SEED2=M`: parse output dumps of simulation with RNG seeds `N` to `M` to generate statistics

## Sample Run

![sample_run](https://raw.githubusercontent.com/sabbirahm3d/epidemic-sim/master/docs/media/sample-full.gif)
