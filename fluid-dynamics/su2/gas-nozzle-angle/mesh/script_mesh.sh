#!/usr/bin/env bash
# Note: it is extruded 1-cell thick, thus 3D.

gmsh nozzle_2d.geo -3 -format cgns
gmsh nozzle_2d.geo -3 -format su2

gmsh nozzle_3d.geo -3 -format cgns
gmsh nozzle_3d.geo -3 -format su2

gmsh domain_2d.geo -3 -format cgns
gmsh domain_2d.geo -3 -format su2

gmsh domain_3d.geo -3 -format cgns
gmsh domain_3d.geo -3 -format su2