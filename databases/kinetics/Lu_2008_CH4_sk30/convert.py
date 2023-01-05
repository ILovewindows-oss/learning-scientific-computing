# -*- coding: utf-8 -*-
# http://spark.engr.uconn.edu/mechs/mechs.htm
from cantera.ck2cti import convertMech
from majordome.simulate.sutherland import fit_sutherland

convertMech(
    "chem.inp", 
    thermoFile="therm.dat",
    transportFile="tran.dat",
    surfaceFile=None,
    phaseName="gas",
    outName="lu30_gri30.cti",
    quiet=False,
    permissive=None,
)

fit_sutherland(
    "lu30_gri30.cti", 
    space=(300, 3000, 100),
    phase="gas",
    plot_all=True,
    outdir="sutherland"
)
