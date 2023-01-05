#!/usr/bin/env bash
chemkinToFoam -newFormat \
    chem.inp  \
    therm.dat \
    transport.foam  \
    OF-hydrocarbon-zhukov-2018-mech.foam \
    OF-hydrocarbon-zhukov-2018-ther.foam
