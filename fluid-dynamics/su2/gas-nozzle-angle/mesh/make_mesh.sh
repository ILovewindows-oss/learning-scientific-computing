#!/usr/bin/env bash
gmsh nozzle_2d.geo -2 -format cgns
gmsh nozzle_2d.geo -2 -format su2

gmsh nozzle_3d.geo -3 -format cgns
gmsh nozzle_3d.geo -3 -format su2

gmsh domain_3d.geo -3 -format cgns
gmsh domain_3d.geo -3 -format su2