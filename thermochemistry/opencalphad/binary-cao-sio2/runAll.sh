#!/usr/bin/env bash
rm -rf dumps/*.LOG dumps/*.plt dumps/*.png

OCEXE="mpiexec -np 4 oc6P"

# OK
# ${OCEXE} macro-01-unary-cao.ocm

# OK
# ${OCEXE} macro-02-unary-cao.ocm

# NOK
# ${OCEXE} macro-03-unary-sio2.ocm

# NOK
# ${OCEXE} macro-04-unary-sio2.ocm

# NOK
# ${OCEXE} macro-05-unary-sio2.ocm
