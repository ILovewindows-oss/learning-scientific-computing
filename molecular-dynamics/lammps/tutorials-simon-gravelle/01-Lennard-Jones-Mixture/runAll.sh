#!/usr/bin/env bash
export OMP_NUM_THREADS=2
PARALLEL="mpiexec -np 4"
${PARALLEL} lmp -in input-step-1.lammps
${PARALLEL} lmp -in input-step-2.lammps
${PARALLEL} lmp -in input-step-3.lammps
