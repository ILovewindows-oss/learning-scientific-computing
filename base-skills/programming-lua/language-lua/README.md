# Lua

This is a Lua distribution aimed to be compiled in any platform with support to CMake and the C-language. It is not a mirror of the main Lua distribution but tries to be kept up-to-date with that source. It is intended to be used in a local environment or installed manually from the generated `dist/` directory. The main goal of this is provide a working version of Lua for teaching under Windows environment. Tests were borrowed from [LuaDist](https://github.com/LuaDist/lua).

## Licence

Check project official licence which is replicated in this distribution (here)[https://www.lua.org/license.html].

**NOTE:** this sub-directory overrides the main repository licence, replacing it by the one contained in it.

## Compiling under *nix* systems

Generate the make files with `cmake -S lua/ -B build/` and then run `make` from the `build/` directory. The options from main Lua build were removed for simplicity.

## Compiling under Windows

Launch a Developer Command Prompt for Visual Studio. From this same directory run `build.bat` and the distribution will be provided in a folder `dist/`. *Notice that this requires Visual Studio with support to C++ to be available. Running from a normal terminal will not work because VS does not place its development executables on the system path*.
