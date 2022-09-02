# Note: it is extruded 1-cell thick, thus 3D.

gmsh.exe nozzle_2d.geo -3 -format cgns -o generated/nozzle_2d.cgns
gmsh.exe nozzle_2d.geo -3 -format su2  -o generated/nozzle_2d.su2

gmsh.exe nozzle_3d.geo -3 -format cgns -o generated/nozzle_3d.cgns
gmsh.exe nozzle_3d.geo -3 -format su2  -o generated/nozzle_3d.su2

gmsh.exe domain_2d.geo -3 -format cgns -o generated/domain_2d.cgns
gmsh.exe domain_2d.geo -3 -format su2  -o generated/domain_2d.su2

gmsh.exe domain_3d.geo -3 -format cgns -o generated/domain_3d.cgns
gmsh.exe domain_3d.geo -3 -format su2  -o generated/domain_3d.su2