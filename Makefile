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
	@$(call iecho,"Generating files for plague-sim...")
	python generate_bbox.py systemc && mv blackboxes systemc
	python generate_bbox.py pyrtl && mv blackboxes pyrtl
	python generate_bbox.py chisel && mv blackboxes chisel

.PHONY: install
.ONESHELL:
install: generate
	mkdir -p build
	cd build && cmake -DCMAKE_CXX_COMPILER=${CXX} .. && $(MAKE)
	mv ../chisel/blackboxes/build.sbt .
	cat <<EOF >> build.sbt
	sourcesInBase := false
	scalaSource in Compile := baseDirectory.value / "../chisel"
	EOF
	sst-register plague-sim plague-sim_LIBDIR=$(CURDIR)

.PHONY: run-sst
.ONESHELL:
run-sst:
	@$(call iecho,"Running plague-sim simulation...")
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
	sst-register -u plague-sim
	@$(call iecho,"Removing cached files...")
	find . -name "*.pyc" -type f -delete
	find . \( -name "__pycache__" -o -name "cmake-build-debug" \) -type d -exec rm -rf {} +
	@$(call iecho,"Removing black boxes and build files...")
	find . \( -name "blackboxes" -o -name "build" \) -type d -exec rm -rf {} +
