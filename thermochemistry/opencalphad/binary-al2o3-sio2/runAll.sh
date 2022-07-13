#!/usr/bin/env bash
rm -rf dumps/*.LOG dumps/*.plt dumps/*.png

OCEXE="mpiexec -np 4 oc6P"

# OK
${OCEXE} macro-01-unary-al2o3.ocm

# OK
${OCEXE} macro-02-unary-sio2.ocm
