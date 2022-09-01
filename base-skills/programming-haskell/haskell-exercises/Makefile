# Options provided to `stack`
FLAGS := 

# Use this when running as root (e.g. inside a container)
FLAGS += --allow-different-user

# List all files for dependencies.
LIBRARY_FILES := $(find src -name "*.hs")
TESTING_FILES := $(find test -name "*.hs")

all: test

setup:
	apt update && apt install -y libcairo-dev
	stack setup $(FLAGS)

simulate: library
	stack exec $(FLAGS) FurnaceBalance
	stack exec $(FLAGS) Oxidation -- 1e-12 300 1473 0.002 0 150e-09 3 100 0.1

library: $(LIBRARY_FILES)
	stack build $(FLAGS)

test: library $(LIBRARY_FILES) $(TESTING_FILES)
	stack test $(FLAGS)

clean:
	stack clean $(FLAGS)
