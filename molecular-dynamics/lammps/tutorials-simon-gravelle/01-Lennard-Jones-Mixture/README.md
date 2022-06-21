# Lennard-Jones Mixture

This is a relecture of [this](https://lammpstutorials.github.io/tutorials/01-SimpleMolecularSimulation.html) tutorial. It has been decomposed in the following files:

- [input-step-1.lammps](input-step-1.lammps) in this part we simply perform the energy minimization and dump results for later use with different simulations.

- [input-step-2.lammps](input-step-2.lammps) here we reload previously dumped state and apply fixes before running the simulation. It also introduces the concept of variables and how dump them to check the convergence during a simulation. Velocity initialization is performed to ensure consistency of initial temperature.

- [input-step-3.lammps](input-step-3.lammps) modifies previous level to add a force vector to impose flow of particles.
