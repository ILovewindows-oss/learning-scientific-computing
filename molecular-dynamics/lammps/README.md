# lammps-learning

 My learning path towards LAMMPS mastering.

## Running LAMMPS

If running in multithreaded mode (not in parallel), consider setting the number of threads used by OpenMP before executing LAMMPS. This can be done in PowerShell (Windows) with `$env:OMP_NUM_THREADS=8` or in Linux with `export OMP_NUM_THREADS=8` for defining 8 threads per process, for example. To run an input file (useful for checking if it is well formatted even before finishing the preparation) run `lmp -in <file_name>`.

For visualization you will also need [VMD](http://www.ks.uiuc.edu/Research/vmd/) and [OVITO](https://www.ovito.org/).

## Tutorials

### LAMMPS tutorials by Simon Gravelle

The original sources of these tutoriais can be found [here](https://lammpstutorials.github.io/). The following reinterpretations of these simulations were studied here:

- [Simple molecular dynamics](tutorials-simon-gravelle/01-Lennard-Jones-Mixture)
- [Osmosis flow through a porous membrane](tutorials-simon-gravelle/02-Osmosis-Flow-Membrane)
- [Nanoconfined electrolyte](tutorials-simon-gravelle/03-Nanoconfined-Electrolyte)
- [Graphene sheet and CNT](tutorials-simon-gravelle/04-Graphene-Deformation)
