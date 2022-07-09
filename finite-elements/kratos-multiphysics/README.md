# Kratos Multiphysics

Notice that before starting here you are recommended to check the [tutorial](https://github.com/KratosMultiphysics/Kratos/wiki/Python-Tutorials). One important point for exporting complex meshes from other tools (thus requiring to add new variables for the solution, ...) is the manipulation as described [here](https://github.com/KratosMultiphysics/Kratos/wiki/Python-Script-Tutorial:-Reading-ModelPart-From-Input-File). Most tutorials listed below were reworked to run with Kratos Multiphysics 9.1 or for coding style/organization reasons.

Here you will find the following tutorials/cases in Python:

- [Input files and IO](02-Input-Files-and-IO): this is a reconstruction of the tutorial initially found [here](https://github.com/KratosMultiphysics/Kratos/wiki/Kratos-input-files-and-IO).
- [Cylinder cooling Re=100 Pr=2](02-CHT-Cylinder-Cooling-Re100-Pr2): check folder for sources. Simulates the vortex path behind a initially hot cylinder.
- [Gaussian hill without diffusion](03-Convection-Diffusion-Gaussian-Hill-Explicit): check folder for sources. Simulates the circular pattern movement of a hot source.
- [Gaussian hill with diffusion](04-Convection-Diffusion-Gaussian-Hill-with-Diffusion-Explicit): check folder for sources. Same as previous but with diffusion enabled.

Once you have mastered Python API, it is recommended to follow the [full C++/Python tutorial for dummies](https://github.com/KratosMultiphysics/Kratos/wiki/Kratos-For-Dummies:-Stationary-heat-transfer) tutorial. It is intended to be a first contact with FEM and the use of Kratos at lower level and development.


## Running in parallel

For running in parallel the libraries must be compiled with [Metis](https://github.com/KratosMultiphysics/Kratos/tree/master/applications/MetisApplication) and [Trilinos](https://github.com/KratosMultiphysics/Kratos/tree/master/applications/TrilinosApplication) support. From a terminal you can simply call `mpiexec -np 4 python3 run.py --with-mpi` to run an application.
