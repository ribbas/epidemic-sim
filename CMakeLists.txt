cmake_minimum_required(VERSION 3.12)
project(epidemic CXX)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR})

# add compiler warnings
add_compile_options(-Wall -Wextra -Wpedantic)

find_package(SIT CONFIG REQUIRED)
if (${SIT_FOUND})

    # -------------------- SST CONFIGS --------------------
    execute_process(
        COMMAND which sst-config
        OUTPUT_VARIABLE SST_CONFIG
        OUTPUT_STRIP_TRAILING_WHITESPACE
    )
    execute_process(
        COMMAND ${SST_CONFIG} --ELEMENT_CXXFLAGS
        OUTPUT_VARIABLE SST_FLAGS
        OUTPUT_STRIP_TRAILING_WHITESPACE
    )
    execute_process(
        COMMAND ${SST_CONFIG} --ELEMENT_LDFLAGS
        OUTPUT_VARIABLE SST_LDFLAGS
        OUTPUT_STRIP_TRAILING_WHITESPACE
    )
    separate_arguments(SST_FLAGS)
    separate_arguments(SST_LDFLAGS)

    execute_process(
        COMMAND which sst-register
        OUTPUT_VARIABLE SST_REGISTER
        OUTPUT_STRIP_TRAILING_WHITESPACE
    )

    execute_process(
        COMMAND which sst
        OUTPUT_VARIABLE SST_BIN
        OUTPUT_STRIP_TRAILING_WHITESPACE
    )

    macro(_sst_compile_link _name)
        if (TARGET ${_name})
            target_compile_definitions(${_name} PRIVATE)
            target_compile_options(${_name} PRIVATE ${SST_FLAGS})
            target_link_options(${_name} PRIVATE ${SST_LDFLAGS})
            execute_process(COMMAND ${SST_REGISTER} ${_name} ${_name}_LIBDIR=${CMAKE_BINARY_DIR})
        endif ()
    endmacro()

    macro(_generate _hdl)
        execute_process(
            COMMAND python ${PROJECT_SOURCE_DIR}/generate_bbox.py ${_hdl}
        )
        execute_process(
            COMMAND mv -n blackboxes ${PROJECT_SOURCE_DIR}/${_hdl}
        )
    endmacro()
    # -------------------- SST CONFIGS --------------------

    # -------------------- SYSTEMC CONFIGS --------------------
    set(CMAKE_PREFIX_PATH /opt/systemc)
    find_package(SystemCLanguage CONFIG REQUIRED)
    set(CMAKE_CXX_STANDARD ${SystemC_CXX_STANDARD})
    # -------------------- SYSTEMC CONFIGS --------------------

    _generate(systemc)
    _generate(pyrtl)
    _generate(verilog)
    execute_process(
        COMMAND cp ${PROJECT_SOURCE_DIR}/verilog/blackboxes/flash_mem_driver.py .
        COMMAND make -f ${PROJECT_SOURCE_DIR}/verilog/blackboxes/Makefile.config dumpconfig
    )

    # ------------------ SYSTEMC EXECUTABLES ------------------
    foreach (SYSC_MOD minf sc_floor sc_mul mul_inv)
        add_executable(${SYSC_MOD}.o ${PROJECT_SOURCE_DIR}/systemc/blackboxes/${SYSC_MOD}_driver.cpp)
        target_link_libraries(${SYSC_MOD}.o SystemC::systemc)
    endforeach ()
    # ------------------ SYSTEMC EXECUTABLES ------------------

    # -------------------- SST EXECUTABLES --------------------
    add_executable(
            libepidemic.so
            epidemic.cpp
            ${PROJECT_SOURCE_DIR}/verilog/blackboxes/flash_mem_comp.cpp
            ${PROJECT_SOURCE_DIR}/pyrtl/blackboxes/mutation_comp.cpp
            ${PROJECT_SOURCE_DIR}/systemc/blackboxes/mul_inv_comp.cpp
            ${PROJECT_SOURCE_DIR}/systemc/blackboxes/minf_comp.cpp
            ${PROJECT_SOURCE_DIR}/systemc/blackboxes/sc_floor_comp.cpp
            ${PROJECT_SOURCE_DIR}/systemc/blackboxes/sc_mul_comp.cpp
    )
    _sst_compile_link(libepidemic.so)
    # -------------------- SST EXECUTABLES --------------------
    if (NOT START_SEED)
        set(START_SEED 0)
    endif()

    if (NOT END_SEED)
        set(END_SEED 0)
    endif()

    add_custom_target(run
        COMMAND ${SST_BIN} ${PROJECT_SOURCE_DIR}/run.py ${START_SEED} ${END_SEED}
    )

    add_custom_target(stats
        COMMAND mkdir -p ${PROJECT_SOURCE_DIR}/data
        COMMAND python ${PROJECT_SOURCE_DIR}/stats/parsemem.py ${START_SEED} ${END_SEED}
    )

    add_custom_target(plot
        COMMAND python ${PROJECT_SOURCE_DIR}/stats/plot.py data/${START_SEED}.json
    )

    unset(START_SEED CACHE)
    unset(END_SEED CACHE)

endif()
