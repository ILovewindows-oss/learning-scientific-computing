# Compilation instructions

## GKLib

```bash
git clone https://github.com/KarypisLab/GKlib.git
cd GKlib
make config cc=mpicc openmp=set prefix=$HOME/Apps/
make && make install
```

## METIS

```bash
git clone https://github.com/KarypisLab/METIS.git
cd METIS
make config cc=mpicc openmp=set shared=1 prefix=$HOME/Apps/ i64=1 r64=1
make && make install
```

## ParMETIS

```bash
git clone https://github.com/KarypisLab/ParMETIS.git
cd ParMETIS

# NOTE: workaround because of compiler raising error!
sed -i "s|-Werror||g" conf/gkbuild.cmake

make config cc=mpicc openmp=set shared=1 prefix=$HOME/Apps/
make && make install
```

## HDF5

```bash
git clone https://github.com/HDFGroup/hdf5.git
```

## CGNS

```bash
git clone -b master https://github.com/CGNS/CGNS.git
```

## Scotch

```
git clone https://gitlab.inria.fr/scotch/scotch.git
```