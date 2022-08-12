// rk4.h
//
#ifndef __rk4__
#define __rk4__

#include "rk4.h"

// Type definition for right-hand-side functions.
typedef void (*RhsType)(const double, const double*, double*, const int, void*);

// Structure allocated for solver data.
typedef struct {
    int size;
    double tstep;
    double* k1;
    double* k2;
    double* k3;
    double* k4;
    double* yval;
    double* ydot;
    double* ytmp;
} Rk4SolverData;

// Function interfaces.
void rk4_init(Rk4SolverData*, int, double );
void rk4_free(Rk4SolverData*);
void rk4_step(Rk4SolverData*, RhsType, double, void*);

#endif // (__rk4__)