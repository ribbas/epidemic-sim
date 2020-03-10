cmake_minimum_required(VERSION 3.12)
project(epidemic CXX)
include(../../tests/CMakeLists.txt)

# add compiler warnings
add_compile_options(-Wall -Wextra -Wpedantic)

# -------------------- SYSTEMC CONFIGS --------------------
set(CMAKE_PREFIX_PATH /opt/systemc)
find_package(SystemCLanguage CONFIG REQUIRED)
set(CMAKE_CXX_STANDARD ${SystemC_CXX_STANDARD})
# -------------------- SYSTEMC CONFIGS --------------------

# ------------------ SYSTEMC EXECUTABLES ------------------
foreach (SYSC_MOD minf sc_floor sc_mul mul_inv)
    add_executable(${SYSC_MOD}.o systemc/blackboxes/${SYSC_MOD}_driver.cpp)
    target_link_libraries(${SYSC_MOD}.o SystemC::systemc)
endforeach ()
# ------------------ SYSTEMC EXECUTABLES ------------------

# -------------------- SST EXECUTABLES --------------------
add_executable(
        libepidemic.so
        epidemic.cpp
        chisel/blackboxes/flash_mem_comp.cpp
        pyrtl/blackboxes/mutation_comp.cpp
        systemc/blackboxes/mul_inv_comp.cpp
        systemc/blackboxes/minf_comp.cpp
        systemc/blackboxes/sc_floor_comp.cpp
        systemc/blackboxes/sc_mul_comp.cpp
)
_sst_compile_link(libepidemic.so)
# -------------------- SST EXECUTABLES --------------------
