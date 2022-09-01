# Learning Scientific Computing

Study materials for general scientific computing matters.

If you are here, maybe you are also interested in the event list from [PRACE](https://events.prace-ri.eu/).

More about my projects in my personal [Github.io Page](https://wallytutor.github.io/).

[Majordome](https://python-majordome.readthedocs.io/en/latest/index.html) is the Python package where you find boilerplate code that is used all across this repository.

---

## Programming

If you are starting, Excercism is a nice entry-point:

- [Exercism](https://exercism.org/dashboard)

### C++

### Cuda

- [NGC Catalog NVIDIA](https://catalog.ngc.nvidia.com/)

### Fortran

### Haskell

- [GHCup](https://www.haskell.org/ghcup/)
- [Haskell for Numerics?](https://idontgetoutmuch.wordpress.com/2017/06/02/1090/)
- [Course by Dmitrii Kovanikov](https://github.com/haskell-beginners-2022/course-plan)

### Julia

### Lisp

### Octave

### Python

- [8 surprising ways how to use Jupyter Notebook](https://mljar.com/blog/how-to-use-jupyter-notebook/)

Some (yet crude) visual programming in Python:

- [Barfi](https://barfi.readthedocs.io/en/latest/)
- [nodezator](https://nodezator.com/)

### Rust

Rust community often organizes *books* on the main topics regarding the language:

- [Rust Book](https://doc.rust-lang.org/book/)
- [The Cargo Book](https://doc.rust-lang.org/cargo/index.html)
- [The rustup book](https://rust-lang.github.io/rustup/index.html)
- [Rust Cookbook](https://rust-lang-nursery.github.io/rust-cookbook/intro.html)

Some resources for learning Rust (start with *rustlings*):

- [rustlings](https://github.com/rust-lang/rustlings/)
- [Rust By Example](https://doc.rust-lang.org/stable/rust-by-example/)
- [Rust Playground](https://play.rust-lang.org/)

Useful links for working with `cargo`:

- [Bundle Cargo](https://stackoverflow.com/questions/67562843/)
- [The Manifest Format](https://doc.rust-lang.org/cargo/reference/manifest.html)

Useful links for doing numerical stuff in Rust:

- [Vec in std::vec - Rust](https://doc.rust-lang.org/std/vec/struct.Vec.html)
- [plotters](https://docs.rs/plotters/latest/plotters/)

### Scilab

### Other programming materials

- [Why Futhark?](https://futhark-lang.org/index.html)

---

## Support software

### Linux

### Git

### Gnuplot

### LaTeX

---

### Pre- and Postprocessing

### Gmsh

[Gmsh](https://gmsh.info/) is an open source meshing tool. Recommended for existing geometries and 2D cases (if CAD is required). Tool can provide both structured or unstructured meshes with a little effort. It provides its own C-like language and Python API.

### Salome Platform

[Salome Platform](https://www.salome-platform.org/) is an open source scientific computation environment. It has strong CAD functionalities and meshing. It can also be interfaced to other EDF applications. Its documentation can be found [here](https://docs.salome-platform.org/latest/main/index.html).

### Blender

[Blender](https://www.blender.org/) has nothing to do with scientific computation but is a good tool for generating (complex) geometries and STL files for use with meshing tools such as `snappyHexMesh`. Its documentation can be found [here](https://docs.blender.org/manual/en/latest/getting_started/index.html).

### ParaView

[ParaView](https://www.paraview.org/) is the *de facto* open source post-processing tool for scientific computations. Its documentation can be found [here](https://docs.paraview.org/en/latest/).

Other links:

- [Video tutorial by Cyprien Rusu](https://www.youtube.com/playlist?list=PLvkU6i2iQ2fpcVsqaKXJT5Wjb9_ttRLK-)
- [Video tutorial at TuxRiders](https://www.youtube.com/playlist?list=PL6fjYEpJFi7W6ayU8zKi7G0-EZmkjtbPo)

---

## System Modeling

### Modelica

- [Modelica Association](https://modelica.org/index.html)
- [OpenModelica (FOSS implementation)](https://www.openmodelica.org/)
- [Modelica 4.0 documentation](https://doc.modelica.org/Modelica%204.0.0/Resources/helpDymola/Modelica.html)
- [Modelica University](https://mbe.modelica.university/)

### Dyssol

Dyssol is process unit operations simulator conceived from granular processes.

- [Dyssol repository](https://github.com/FlowsheetSimulation/Dyssol-open)
- [Dyssol documentation](https://flowsheetsimulation.github.io/Dyssol-open/)

### Other software

- [Ascend4 (legacy)](https://ascend4.org/)
- [COCO](https://www.cocosimulator.org/index.html)

---

## Finite Elements

### Elmer

- [Elmer webpage](https://www.csc.fi/web/elmer)

### FEniCS

### FreeFEM++

### GetFEM

### Kratos Multiphysics

- [Kratos webpage](https://github.com/KratosMultiphysics/Kratos)
- [Kratos documentation](https://github.com/KratosMultiphysics/Documentation)
- [Kratos examples](https://github.com/KratosMultiphysics/Examples)
- [Kratos Applications](https://github.com/KratosMultiphysics/Kratos/tree/master/applications)

### Moose

### Nectar++

- [Nectar++ webpage](https://www.nektar.info/)

### GetDP

- [GetDP webpage](https://getdp.info/)

---

## Fluids and Transport

The list below provides useful links for learning transport phenomena simulation:

- [CFD Online (forum)](https://www.cfd-online.com/)
- [NASA Turbulence LARC](https://turbmodels.larc.nasa.gov/)
- [CFD General Notation System (CGNS)](http://cgns.github.io/)
- [CFD Support (list of software)](https://www.cfdsupport.com/cae-open-source-software.html)
- [CFDyna](http://cfdyna.com/)
- [Several student projects](https://hmf.enseeiht.fr/travaux/projnum/book/)

And below you find some supporting tools for setting up a CFD simulation:

- [Y-Plus](https://www.cfd-online.com/Tools/yplus.php)
- [Skin friction](https://www.cfd-online.com/Wiki/Skin_friction_coefficient)
- [Fluid Mechanics 101](https://fluidmechanics101.com/pages/tools.html)

The following is a list of water property calculators for use in detailed simulations:

- [IAPWS-95](http://www.iapws.org/relguide/IAPWS-95.html)
- [iapws](https://iapws.readthedocs.io/en/latest/iapws.iapws95.html)
- [CoolProp](http://www.coolprop.org/)
- [freesteam](http://freesteam.sourceforge.net/)
- [qingfengxia/freesteam](https://github.com/qingfengxia/freesteam)

It is also interesting to have access to some combustion-related materials:

- [Methane/air combustion](https://www.cerfacs.fr/cantera/mechanisms/meth.php)

### Basilisk

- [Basilisk webpage](http://basilisk.fr/)

### Code Saturn and Other EDF software

- [Code Saturne webpage](https://www.code-saturne.org/cms/web/)
- [Code Saturne documentation](https://www.code-saturne.org/documentation/7.1/doxygen/src/index.html)
- [Code Aster webpage](https://www.code-aster.org/V2/spip.php?rubrique1)
- [SYRTHES](https://www.edf.fr/en/the-edf-group/inventing-the-future-of-energy/r-d-global-expertise/our-offers/simulation-softwares/syrthes?logiciel=10818)

### OpenFOAM

OpenFOAM distributions

- [OpenFOAM.org (CFD Direct)](https://openfoam.org/)
- [OpenFOAM.com (ESI)](https://www.openfoam.com/)

General purpose, turorials, and documentation:

- [OpenFOAM Wiki](https://openfoamwiki.net/index.php/Main_Page)
- [TU Wien tutorials](https://www.cfd.at/tutorials)
- [3-week series tutorials](https://wiki.openfoam.com/index.php?title=%223_weeks%22_series)
- [Tutorials by author](https://wiki.openfoam.com/Collection_by_authors)
- [FEA for All tutorials of OpenFOAM](https://feaforall.com/category/tutorial/openfoam/)
- [CEMF tutorials](https://www.cemf.ir/category/tutorials/)

External solvers:

- [catalyticFoam](https://github.com/multiscale-catalysis-polimi/catalyticFoam)
- [CEMF solvers](https://www.cemf.ir/openfoam/cemf-solvers-based-on-openfoam/)

Conjugate heat transfer:

- [Tutorial of chtMultiRegionFoam](https://www.youtube.com/watch?v=Nhhm-ZPxVRc&list=PLykdptEQ2lFintoU5dgerzQbQprd9zwTY)
- [Tutorial - Heat sink](https://www.youtube.com/watch?v=MD3cjOF8S60)

Volume of fluid (VoF):

- [interFoam tutorial - raising bubble](https://www.youtube.com/watch?v=JYHhF25OTm0&list=PLykdptEQ2lFintoU5dgerzQbQprd9zwTY&index=2)

Moving reference frame (MRF):

- [Video tutorial by Asmaa Hadane](https://www.youtube.com/watch?v=KccubqHQS-0)

### SU2

- [SU2 webpage](https://su2code.github.io/)

### OpenSMOKE++

- [OpenSMOKE++ webpage](https://www.opensmokepp.polimi.it/)

### Reduced order modeling (ROM)

- [GeN-ROM paper](https://www.sciencedirect.com/science/article/pii/S0149197022000282)
- [ITHACA-FV ROM for OpenFOAM](https://github.com/mathLab/ITHACA-FV)
- [BYU-PRISM/Seeq](https://github.com/BYU-PRISM/Seeq)

## Lattice-Boltzmann method

The following links provide simple implementations to learn DEM development:

- [LBM in Python from scratch](https://medium.com/swlh/create-your-own-lattice-boltzmann-simulation-with-python-8759e8b53b1c)
- [Repository with implementation samples](https://github.com/jviquerat/lbm)

### Palabos

- [Palabos webpage](https://palabos.unige.ch/)

### pyLBM

- [pyLBM documentation](https://pylbm.readthedocs.io/en/latest/)

---

## Granular Flow

### LIGGGHTS

- [LIGGGHTS webpage](https://www.cfdem.com/liggghts-open-source-discrete-element-method-particle-simulation-code#:~:text=LIGGGHTS%20is%20an%20Open%20Source,the%20field%20of%20Molecular%20Dynamics.)
- [LIGGGHTS documentation](https://www.cfdem.com/media/DEM/docu/Manual.html)

### Yade DEM

- [Yade DEM Documentation](https://yade-dem.org/doc/)

### Project Chrono

- [Project Chrono webpage](https://projectchrono.org/)

### Musen

- [Musen repository](https://github.com/msolids/musen)

---

## Molecular Dynamics and DFT

- [Materials Project](https://materialsproject.org/)
- [Book Hinchliffe](https://www.wiley.com/en-us/Molecular+Modelling+for+Beginners%2C+2nd+Edition-p-9781119964810)
- [Feynman](https://www.feynmanlectures.caltech.edu/)

### LAMMPS

- [LAMMPS](https://www.lammps.org/)
- [LAMMPS Pre-Post](https://www.lammps.org/prepost.html)
- [LAMMPS Visualization](https://www.lammps.org/viz.html)
- [LAMMPS Tutorials](https://www.lammps.org/tutorials.html)
- [LAMMPS Papers](https://www.lammps.org/papers.html)
- [LAMMPS Documentation](https://docs.lammps.org/Manual.html)

### ESPResSo

- [ESPReSo webpage](https://espressomd.org/wordpress/)

### Abinit

- [Abinit webpage](https://www.abinit.org/)

### BigDFT

- [BigDFT](https://bigdft.org/?i=1)

### CP2K

- [CP2K](https://www.cp2k.org/)

### Dirac

- [DIRAC webpage](http://www.diracprogram.org/doku.php/)

### Fleur

- [FLEUR webpage](https://www.flapw.de/MaX-6.0/)

### Gromacs

- [Gromacs webpage](https://www.gromacs.org/)

### Quantum Espresso

- [Quantum Espresso webpage](https://www.quantum-espresso.org/)

### Other molecular dynamics software

- [Dalton/LSDalton](https://daltonprogram.org/)
- [DL_POLY](https://www.scd.stfc.ac.uk/Pages/DL_POLY.aspx)
- [HOOMD](http://glotzerlab.engin.umich.edu/hoomd-blue/)
- [NAMD](https://www.ks.uiuc.edu/Research/namd/)
- [Siesta](https://siesta-project.org/siesta/)
- [Yambo](http://www.yambo-code.org/)

### Molecular dynamics pre-/post-processing

- [colvars](https://colvars.github.io/)
- [VMD](http://www.ks.uiuc.edu/Research/vmd/)
- [MAICoS](https://maicos-devel.gitlab.io/maicos/index.html)
- [TopoTools](https://sites.google.com/site/akohlmey/software/topotools)

---

## Thermophysics

### Cantera

### OpenCALPHAD

### PyCALPHAD

---

## Entering (other software to check)

- [ASL GitHub](https://github.com/AvtechScientific/ASL)
- [Maxima CAS](https://maxima.sourceforge.io/)
- [FDS-SMV Manuals](https://pages.nist.gov/fds-smv/manuals.html)

## Entering (repositories to check)

- [GitHub - firemodels/fds: Fire Dynamics Simulator](https://github.com/firemodels/fds)
- [GitHub - flame-code/FLAME: FLAME: a library for atomistic modeling environments](https://github.com/flame-code/FLAME)
- [stitching/stitching at main · lukasalexanderweber/stitching](https://github.com/lukasalexanderweber/stitching/tree/main/stitching)
- [usnistgov/atomman: Atomistic Manipulation Toolkit](https://github.com/usnistgov/atomman)
- [GrossfieldLab/loos: LOOS: a lightweight object-oriented structure analysis library](https://github.com/GrossfieldLab/loos)
- [glotzerlab/freud: Powerful, efficient particle trajectory analysis in scientific Python.](https://github.com/glotzerlab/freud)
- [GitHub - xiaoh/sediFoam: CFD-DEM Solver with emphasis on sediment transport](https://github.com/xiaoh/sediFoam)
- [GitHub - CoolProp/CoolProp: Thermophysical properties for the masses](https://github.com/CoolProp/CoolProp)
- [GitHub - fwitte/fluprodia: Fluid property diagrams](https://github.com/fwitte/fluprodia)
- [shiftkey/desktop](https://github.com/shiftkey/desktop/releases)
- [bjodah/chempy: A package useful for chemistry written in Python](https://github.com/bjodah/chempy)


<!-- TODO
Courses to follow:
\begin{todolist}
\item\href{https://ocw.mit.edu/courses/mathematics/18-075-advanced-calculus-for-engineers-fall-2004/}{Advanced Calculus}
\item\href{https://ocw.mit.edu/courses/mechanical-engineering/2-06-fluid-dynamics-spring-2013/}{Fluid Dynamics}:
\item\href{https://ocw.mit.edu/courses/mechanical-engineering/2-25-advanced-fluid-mechanics-fall-2013/}{Advanced Fluid Mecanics}
\item\href{https://ocw.mit.edu/courses/mechanical-engineering/2-27-turbulent-flow-and-transport-spring-2002/}{Turbulent Flow and Transport}
\item\href{https://ocw.mit.edu/courses/mechanical-engineering/2-051-introduction-to-heat-transfer-fall-2015/}{Introduction to Heat Transfer}
\item\href{https://ocw.mit.edu/courses/mechanical-engineering/2-51-intermediate-heat-and-mass-transfer-fall-2008/}{Intermediate Heat Transfer}
\item\href{https://ocw.mit.edu/courses/mechanical-engineering/2-58j-radiative-transfer-spring-2006/}{Radiative Transfer}
\item\href{https://ocw.mit.edu/courses/electrical-engineering-and-computer-science/6-336j-introduction-to-numerical-simulation-sma-5211-fall-2003/}{Introduction to Simulation}
\item\href{https://ocw.mit.edu/courses/aeronautics-and-astronautics/16-920j-numerical-methods-for-partial-differential-equations-sma-5212-spring-2003/}{Numerical Methods for PDE}
\item\href{https://ocw.mit.edu/courses/mechanical-engineering/2-29-numerical-fluid-mechanics-spring-2015/}{Numerical Fluid Mechanics}
\item\href{https://ppc.cs.aalto.fi/}{Programming Parallel Computers} (and its extension to \href{https://github.com/parallel-rust-cpp}{Rust})
\item\href{https://www.youtube.com/playlist?list=PLfF--3o8i4r82vJ0kjCVYgqKgyVM5QwN0}{Fluid Mechanics (classical)}
\item\href{https://www.youtube.com/playlist?list=PL6S8U84PCLB27bdd15l1xnTSQKf3AOOoj}{Turbulent mixing conference (ICTP)}
\item\href{https://www.youtube.com/playlist?list=PL80xBr8Wq0b5qXRPwyTxmGDOhO4obKOiC}{Turbulent flows}
\item\href{https://www.youtube.com/playlist?list=PLp0hSY2uBeP8rhCbecD1Icahfbr6GSZ19}{Mathematical methods (ICTP)}
\item\href{https://www.youtube.com/playlist?list=PLp0hSY2uBeP_7jL7uqlsxDmvimK2q6eF5}{Fluid dynamics (ICTP)}
\item\href{https://www.youtube.com/channel/UCYlD7XynaJIBuYvmXlRBtnQ}{Pr. Dr. Carlos Thompson channel}
\end{todolist}
-->
