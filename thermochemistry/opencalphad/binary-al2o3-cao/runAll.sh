#!/usr/bin/env bash
rm -rf dumps/*.LOG dumps/*.plt dumps/*.png

# OK
oc6P macro-01-unary-al2o3.ocm

# OK
oc6P macro-02-unary-cao.ocm

# OK
oc6P macro-03-unary-c3a1.ocm

# NOK
# oc6P macro-04-unary-c1a1.ocm

# NOK
# oc6P macro-05-unary-c1a2.ocm

# OK
oc6P macro-06-unary-c1a6.ocm

# Needs improvement, very bad but...
oc6P macro-07-binary-cao-c3a1.ocm

# Needs improvement, very bad but... better than 7
oc6P macro-08-binary-c3a1-c1a1.ocm

# Needs improvement, very bad but... better than 7
oc6P macro-09-binary-c1a1-c1a2.ocm

# OK
oc6P macro-10-binary-c1a2-c1a6.ocm

# OK
oc6P macro-11-binary-c1a6-al2o3.ocm
