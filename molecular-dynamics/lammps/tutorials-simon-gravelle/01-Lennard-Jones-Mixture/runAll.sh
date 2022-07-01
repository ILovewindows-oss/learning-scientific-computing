#!/usr/bin/env bash
export OMP_NUM_THREADS=2
PARALLEL="mpiexec -np 4"
${PARALLEL} lmp -in input-step-1.lammps -log input-step-1.log
${PARALLEL} lmp -in input-step-2.lammps -log input-step-2.log
${PARALLEL} lmp -in input-step-3.lammps -log input-step-3.log
