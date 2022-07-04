#!/usr/bin/env bash
rm -rf dumps/*.LOG dumps/*.plt dumps/*.png

OCEXE="mpiexec -np 4 oc6P"

# OK
${OCEXE} macro-01-unary-al2o3.ocm

# OK
${OCEXE} macro-02-unary-cao.ocm

# OK
${OCEXE} macro-03-unary-c3a1.ocm

# OK
${OCEXE} macro-04-unary-c1a1.ocm

# OK
${OCEXE} macro-05-unary-c1a2.ocm

# OK
${OCEXE} macro-06-unary-c1a6.ocm

# OK (top down works better)
${OCEXE} macro-07-binary-cao-c3a1.ocm

# OK (top down works better)
${OCEXE} macro-08-binary-c3a1-c1a1.ocm

# OK (very sensitive to start X! Use with care!)
${OCEXE} macro-09-binary-c1a1-c1a2.ocm

# OK
${OCEXE} macro-10-binary-c1a2-c1a6.ocm

# OK
${OCEXE} macro-11-binary-c1a6-al2o3.ocm
