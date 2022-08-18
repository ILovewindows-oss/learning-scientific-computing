#!/usr/bin/env bash

# Configure project build.
cmake -S lua/ -B build/

# Run build from command line.
cd build && make && cd ..

# Create distribution directory.
cd build && make install && cd ..

# Create packages path.
mkdir -p dist/scripts/
cp -avr lua/scripts/* dist/scripts/

# Run all tests.
cd test
../dist/bin/lua bisect.lua
../dist/bin/lua cf.lua
../dist/bin/lua echo.lua a b c
../dist/bin/lua env.lua
../dist/bin/lua factorial.lua
../dist/bin/lua fib.lua
../dist/bin/lua fibfor.lua
# ../dist/bin/lua globals.lua
../dist/bin/lua hello.lua
../dist/bin/lua life.lua
../dist/bin/lua luac.lua life.lua
../dist/bin/lua luac.out
../dist/bin/lua printf.lua
# ../dist/bin/lua readonly.lua
../dist/bin/lua sieve.lua
../dist/bin/lua sort.lua
# ../dist/bin/lua table.lua
../dist/bin/lua trace-calls.lua
# ../dist/bin/lua trace-globals.lua
# ../dist/bin/lua xd.lua
cd ..