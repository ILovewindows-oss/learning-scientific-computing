CC       := gcc
AR       := ar

CPPFLAGS := -Wall -Werror -O3 -g -Iinclude -Llib
ARFLAGS  := -crs

all: lib

lib: static shared

samples: lib sample_static sample_shared

static: rk4
	$(AR) $(ARFLAGS) lib/librk4.a src/rk4.o

shared: rk4
	$(CC) -shared -o lib/librk4.so src/rk4.o

sample_static: static samples/sample.c
	$(CC) $(CPPFLAGS) -o sample_static.exe samples/sample.c lib/librk4.a

sample_shared: shared samples/sample.c
	$(CC) $(CPPFLAGS) -o sample_shared.exe samples/sample.c -lrk4

rk4: src/rk4.c include/rk4.h
	$(CC) $(CPPFLAGS) -c -fpic -Iinclude src/rk4.c -o src/rk4.o

run: samples
	./sample_static.exe > data/results_static.dat
	LD_LIBRARY_PATH=lib ./sample_shared.exe > data/results_shared.dat

clean:
	rm -rf data/*.dat lib/*.so lib/*.a src/*.o *.exe
