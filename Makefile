MAKEFLAGS += --no-print-directory
BASE_DIR = $(CURDIR)

define iecho
	echo "\e[1;34m$1\e[0m"
endef

define eecho
	echo "\e[1;31m$1\e[0m"
endef

.PHONY: generate
generate:
	@$(call iecho,"Generating files for epidemic-sim...")
	python generate_bbox.py systemc && mv -n blackboxes systemc
	python generate_bbox.py pyrtl && mv -n blackboxes pyrtl
	python generate_bbox.py verilog && mv -n blackboxes verilog

.PHONY: install
.ONESHELL:
install:
	@mkdir -p build
	cd build && cmake -DCMAKE_CXX_COMPILER=${CXX} .. && $(MAKE)
	cp ../verilog/blackboxes/flash_mem_driver.py .
	$(MAKE) -f ../verilog/blackboxes/Makefile.config dumpconfig
	sst-register epidemic-sim epidemic-sim_LIBDIR=$(CURDIR)

.PHONY: run
.ONESHELL:
run:
	@$(call iecho,"Running epidemic-sim simulation...")
	cd build && sst ../run.py ${SEED} || { $(call eecho,"SST failed to launch properly - make sure to clear the cache"); exit 1; }

.PHONY: stats
stats:
	@mkdir -p data
	@python stats/parsemem.py build/${SEED}.txt ${SEED}

.PHONY: plot
plot:
	@python stats/plot.py data/${SEED}.json

.PHONY: clean
# unregister SST components and remove all compiled objects and cached files
clean:
	@$(call iecho,"Unregistering components...")
	sst-register -u epidemic-sim
	@$(call iecho,"Removing cached files...")
	find . -name "*.pyc" -type f -delete
	find . \( -name "__pycache__" -o -name "cmake-build-debug" \) -type d -exec rm -rf {} +
	@$(call iecho,"Removing black boxes and build files...")
	find . \( -name "blackboxes" -o -name "build" \) -type d -exec rm -rf {} +
