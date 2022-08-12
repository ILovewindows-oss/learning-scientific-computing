// rk4.c
//
#include "rk4.h"
#include <stdlib.h>

void rk4_init(Rk4SolverData* solver_data, int size, double tstep)
{
    solver_data->size = size;
    solver_data->tstep = tstep;

    solver_data->k1 = (double*)malloc(size * sizeof(double));
    solver_data->k2 = (double*)malloc(size * sizeof(double));
    solver_data->k3 = (double*)malloc(size * sizeof(double));
    solver_data->k4 = (double*)malloc(size * sizeof(double));

    solver_data->yval = (double*)malloc(size * sizeof(double));
    solver_data->ydot = (double*)malloc(size * sizeof(double));
    solver_data->ytmp = (double*)malloc(size * sizeof(double));
}


void rk4_free(Rk4SolverData* solver_data)
{
    free(solver_data->k1);
    free(solver_data->k2);
    free(solver_data->k3);
    free(solver_data->k4);
    free(solver_data->yval);
    free(solver_data->ydot);
    free(solver_data->ytmp);
}


void rk4_step(Rk4SolverData *solver_data, RhsType f,
              double t, void* data)
{
    double dt = solver_data->tstep;

    // STEP 1 -> k1

    f(t, solver_data->yval, solver_data->ydot,
      solver_data->size, data);

    for (int i = 0; i != solver_data->size; i++)
    {
        solver_data->k1[i] = solver_data->ydot[i];
        solver_data->ytmp[i] = solver_data->yval[i]
          + dt * solver_data->ydot[i] / 2.0;
    }

    // STEP 2 -> k2

    f(t + dt / 2.0, solver_data->ytmp, solver_data->ydot,
      solver_data->size, data);

    for (int i = 0; i != solver_data->size; i++)
    {
        solver_data->k2[i] = solver_data->ydot[i];
        solver_data->ytmp[i] = solver_data->yval[i]
          + dt * solver_data->k2[i] / 2.0;
    }

    // STEP 3 -> k3

    f(t + dt / 2.0, solver_data->ytmp, solver_data->ydot,
      solver_data->size, data);

    for (int i = 0; i != solver_data->size; i++)
    {
        solver_data->k3[i] = solver_data->ydot[i];
        solver_data->ytmp[i] = solver_data->yval[i]
          + dt * solver_data->k3[i] / 2.0;
    }

    // STEP 4 -> k4

    f(t + dt, solver_data->ytmp, solver_data->ydot,
      solver_data->size, data);

    for (int i = 0; i != solver_data->size; i++)
    {
        double k1 = solver_data->k1[i];
        double k2 = solver_data->k2[i];
        double k3 = solver_data->k3[i];
        double k4 = solver_data->ydot[i];

        solver_data->k4[i] = k4;  // Not really necessary!
        solver_data->yval[i] += (k1 +  2 * k2 + 2 * k3 + k4) * dt / 6.0;
    }
}
