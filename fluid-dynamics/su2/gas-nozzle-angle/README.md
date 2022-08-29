---
title: "Simulation of burner nozzle velocity"
author: Walter Dal'Maz Silva
date: August 25, 2022
geometry: margin=2cm
output: pdf_document
---

# Simulation of burner nozzle velocity

## Goal

Compute exit angle of ejected gas stream and velocity.

## Conditions

Flow of methane through the nozzle with the following conditions:

| Quantity              | Units | Case 1 | Case 2 |
| --------------------- | ----- | ------ | ------ |
| Inlet temperature     | K     | 298.15 | 298.15 |
| Inlet flow rate       | kg/h  | 322    | 48.7   |
| Inlet pressure (ref)  | mbar  | 280    | 20     |

Notice that in 2D cases, since each jet is 6 mm wide, the mass flow rate needs to be scaled for the equivalent value of 1000 mm because of the loss of one dimension. Since there are 8 jets in the burner the value needs to be computed on a jet basis. The actual value for 2D case 1 is 6708.3 kg/(h.m) and for case 2 it is 1014.6 kg/(h.m). This is required so that jet velocity is equivalent to 3D cases.

## Hypothesis and equations

- First 2D and then a 3D axisymmetric case.
- Gas flows only through slots (perfect sealing of round surfaces).
- Pure substance (air dilution effects neglected outside nozzle).
- Compressible flow (implied energy equation).
- Turbulence handling with a k-omega SST model.
- No gravitational effects.

**NOTE:** there is a small gap of 0.24 mm in the round surface considered with perfect sealing, but modeling this through CFD would require a prohibitively large grid and other complications associated with the compressible conditions. This was already taken into account in 2D boundary conditions calculations.

## Geometry and mesh

Geometry was provided in a DWG file and reconstructed with Space Claim. All cases will be run with same geometry of perfectly aligned nozzle setting, as provided in Figure \ref{fig:geometry}.

 ![Geometry of burner nozzle\label{fig:geometry}](data/geometry.png "Geometry of burner nozzle")

From the measured coordinates Figure \ref{fig:mesh-su2} fully structured grid was established for 2D cases.

 ![Mesh of burner nozzle (SU2)\label{fig:mesh-su2}](mesh/gmsh-v2-2D-flat/mesh.png "Mesh of burner nozzle (SU2)")

Also for 2D simulations, but with OpenFOAM, an extruded version of mesh with one cell in thickness is produced as depicted in Figure \ref{fig:mesh-of}.

 ![Mesh of burner nozzle (OpenFOAM)\label{fig:mesh-of}](mesh/gmsh-v2-2D-volume/mesh.png "Mesh of burner nozzle (OpenFOAM)")

## Material properties

Since high velocities are present, a compressible ideal gas law is used for density.

Other propeties are reported in the following figure (Cantera + Gri-Mech 3.0).

 ![Material properties (methane).](data/properties.png "Material properties (methane).")

## Solution procedure

**TODO:** Benchmark between Fluent, OpenFOAM, and SU2 for 2D case

**TODO:** Fluent or OpenFOAM simulation in 3D case.

## Validated tools

- gmsh v4.9.5
- SU2 v7.4.0
- OpenFOAM
- Fluent

## Summary

- Simulations in 2D: 2 cases x 3 software, 6 simulations.
- Simulations in 3D: 2 cases x 1 software, 2 simulations.
