gmsh.exe nozzle_2d.geo -2 -format cgns
gmsh.exe nozzle_2d.geo -2 -format su2

gmsh.exe nozzle_3d.geo -3 -format cgns
gmsh.exe nozzle_3d.geo -3 -format su2

# Note: it is extruded 1-cell thick, thus 3D.
gmsh.exe domain_2d.geo -3 -format cgns
gmsh.exe domain_2d.geo -3 -format su2

gmsh.exe domain_3d.geo -3 -format cgns
gmsh.exe domain_3d.geo -3 -format su2