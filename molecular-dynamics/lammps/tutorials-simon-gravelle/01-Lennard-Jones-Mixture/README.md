# Lennard-Jones Mixture

This is a relecture of [this](https://lammpstutorials.github.io/tutorials/01-SimpleMolecularSimulation.html) tutorial. It has been decomposed in the following files:

- [input-step-1.lammps](input-step-1.lammps) in this part we simply perform the energy minimization and dump results for later use with different simulations.

- [input-step-2.lammps](input-step-2.lammps) here we reload previously dumped state and apply fixes before running the simulation. It also introduces the concept of variables and how dump them to check the convergence during a simulation. Velocity initialization is performed to ensure consistency of initial temperature.

- [input-step-3.lammps](input-step-3.lammps) modifies previous level to add a force vector to impose flow of particles.

Paralellization tests have shown that script [input-step-2.lammps](input-step-2.lammps) runs in approximately 210 s with a single processor, 110 s with 2 processors and 80 s with 4 processors. Results (time series plotted with [post-step-2.py](post-step-2.py) and pair energy) are not exaclty the same though (reasons to be investigated, probably due to the core communication rate).
