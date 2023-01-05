#!/usr/bin/env bash
chemkinToFoam -newFormat \
    chem.inp  \
    therm.dat \
    transport.foam  \
    OF-hydrocarbon-lu-2008-sk30-mech.foam \
    OF-hydrocarbon-lu-2008-sk30-ther.foam
