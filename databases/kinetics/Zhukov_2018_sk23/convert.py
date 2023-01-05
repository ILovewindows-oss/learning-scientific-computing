# -*- coding: utf-8 -*-
# http://spark.engr.uconn.edu/mechs/mechs.htm
from cantera.ck2cti import convertMech

convertMech(
    "chem.inp", 
    thermoFile="therm.dat",
    transportFile="tran.dat",
    surfaceFile=None,
    phaseName="gas",
    outName="zhukov23_gri30.cti",
    quiet=False,
    permissive=None,
)

convertMech(
    "chem.inp", 
    thermoFile="therm_alt.dat",
    transportFile="tran_alt.dat",
    surfaceFile=None,
    phaseName="gas",
    outName="zhukov23_gri30_alt.cti",
    quiet=False,
    permissive=None,
)

