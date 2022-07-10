##############################################################################
## Makefile
##############################################################################

CXX := /usr/bin/g++
FOR := /usr/bin/gfortran
AR  := /usr/bin/ar

CPPFLAGS := -g -O3 -std=c++11 -Wall -Iinclude
FFLAGS   := -g -O3 -m64 -std=f2008ts -Ilib -Jlib
ARFLAGS  := sq
RM       := rm -rf

all: f_example.exe c_example.exe

c_example.exe: lib/libCExample.a src/c_example.cpp
	$(CXX) $(CPPFLAGS) src/c_example.cpp lib/libCExample.a -lgfortran -o c_example.exe

f_example.exe: lib/libFExample.a src/f_example.f95
	$(FOR) $(FFLAGS) src/f_example.f95 lib/libFExample.a -o f_example.exe

lib/module_c_example.o: src/module_c_example.f95
	$(FOR) $(FFLAGS) -c src/module_c_example.f95 -o lib/module_c_example.o

lib/module_f_example.o: src/module_f_example.f95
	$(FOR) $(FFLAGS) -c src/module_f_example.f95 -o lib/module_f_example.o

lib/libFExample.a: lib/module_f_example.o
	$(AR) $(ARFLAGS) lib/libFExample.a lib/module_f_example.o

lib/libCExample.a: lib/module_f_example.o lib/module_c_example.o
	$(AR) $(ARFLAGS) lib/libCExample.a lib/module_f_example.o lib/module_c_example.o

clean:
	$(RM) *.exe lib/*.a lib/*.mod lib/*.o src/*.mod

##############################################################################
## EOF
##############################################################################
