#include <stdlib.h>
#include <stdio.h>
#include "rk4.h"

static void f(
    const double t,   // Physical time [s]
    const double* y,  // Problem state [-]
    double* ydot,     // Right-hand side [-/s]
    const int size,   // Problem size [-]
    void* data)       // User data (not used)
{
    ydot[0] = -1.0 * y[0];
}

int main()
{
    // Problem size.
    int size = 1;

    // Integration end time [s].
    double tend = 10.0;

    // Integration time step [s].
    double tstep = 0.1;

    // Number of integration steps.
    int no_steps = (int)(tend / tstep);

    // User supplied data (if any).
    void* user_data = NULL;

    // Solver memory.
    Rk4SolverData* solver_data = NULL;

    // Allocate solver memory.
    solver_data = (Rk4SolverData*)malloc(sizeof(Rk4SolverData));

    // Allocate solver internal memory.
    rk4_init(solver_data, size, tstep);

    // Provide initial condition.
    solver_data->yval[0] = 1.0;

    // Print initial state.
    printf("%.6f\t%.6f\n", 0.0, solver_data->yval[0]);

    // Integrate problem over steps.
    for (int i = 0; i != no_steps; i++)
    {
        const double t = i * tstep;
        rk4_step(solver_data, f, t, user_data);

        printf("%.6f\t%.6f\n", t + tstep, solver_data->yval[0]);
    }
    
    // Deallocate all.
    rk4_free(solver_data);
    free(solver_data);

    return 0;
}