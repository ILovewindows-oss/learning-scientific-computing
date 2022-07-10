# Using Fortran from C/C++

Simple example of Fortran usage from C/C++ programs.

This example is not yet exhaustive and will eventually be updated.

Recommended reading [here](https://stackoverflow.com/tags/fortran-iso-c-binding/info).

## Sequence of development

1. Fortran development:
   - Write Fortran [module](src/module_f_example.F95)
   - Write Fortran ISO-C binding [module](src/module_c_example.F95)

2. Libraries generation (in this order):
   - Compile Fortran modules as object files
   - Archive Fortran objects as a library
   - Compile Fortran ISO-C binding modules as object files
   - Archive Fortran ISO-C binding objects as a library 

3. Fortran testing:
   - Write Fortran [program](src/f_example.F95) for testing the library
   - Compile Fortran executable and link to the Fortran library

4. C/C++ testing:
   - Write C/C++ [header](include/c_example.hpp) with interfaces from Fortran ISO-C binding
   - Write C/C++ [program](src/c_example.cpp) for testing the library
   - Compile C/C++ executable and link to Fortran ISO-C binding library

## Compiling

### Fortran code

Compile Fortran code using standard `-std=f2008ts`, allowing Technical Specification (TS) 29113 on Further Interoperability of Fortran with C. For details please check [here](https://gcc.gnu.org/onlinedocs/gcc-4.8.0/gfortran/Fortran-Dialect-Options.html).

### C/C++ code

Nothing unusual is required for pre-processor flags. For compatibility with Fortran calls, it is necessary to add `-lgfortran` to the linker.

### Build

Just run `make` and it should compile out-of-the box under Nix systems provided a C++ (C++11 compatible) and a Fortran (f2008ts compatible) compilers are available and `make` is installed.
