#!/usr/bin/env bash
# Note: it is extruded 1-cell thick, thus 3D.

gmsh nozzle_2d.geo -3 -format cgns -o generated/nozzle_2d.cgns
gmsh nozzle_2d.geo -3 -format su2  -o generated/nozzle_2d.su2

gmsh nozzle_3d.geo -3 -format cgns -o generated/nozzle_3d.cgns
gmsh nozzle_3d.geo -3 -format su2  -o generated/nozzle_3d.su2

gmsh domain_2d.geo -3 -format cgns -o generated/domain_2d.cgns
gmsh domain_2d.geo -3 -format su2  -o generated/domain_2d.su2

gmsh domain_3d.geo -3 -format cgns -o generated/domain_3d.cgns
gmsh domain_3d.geo -3 -format su2  -o generated/domain_3d.su2
