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
git checkout hdf5-1_10_6

./configure --prefix=$HOME/Apps/local/ \
    --enable-build-mode=production \
    --enable-fortran=yes \
    --enable-cxx=yes \
    --enable-hl=yes \
    --enable-tests=yes \
    --enable-tools=yes \
    --enable-shared=yes \
    --enable-static=yes \
    --enable-optimization=high \
    --enable-parallel=no

make -j40 && make install

# Also consider running tests.
# make test
```

## CGNS

```bash
sudo apt install -y tcl8.6-dev tk8.6-dev

git clone -b master https://github.com/CGNS/CGNS.git
cd CGNS && mkdir build && cd build

cmake \
    -DCMAKE_PREFIX_PATH=$HOME/Apps/local/ \
    -DCGNS_BUILD_CGNSTOOLS=true \
    -DCGNS_BUILD_SHARED=true \
    -DCGNS_BUILD_TESTING=true \
    -DCGNS_ENABLE_64BIT=true \
    -DCGNS_ENABLE_FORTRAN=true \
    -DCGNS_ENABLE_HDF5=true \
    -DCGNS_ENABLE_TESTS=true \
    -DCGNS_USE_SHARED=true \
    -DCMAKE_BUILD_TYPE=Release \
    -DHDF5_DIR=$HOME/Apps/local/lib \
    -DHDF5_NEED_MPI=false \
    -DHDF5_NEED_ZLIB=false \
    -DHDF5_NEED_SZIP=false \
    -DFORTRAN_NAMING=LOWERCASE_ \
    ..
```

## Scotch

```
git clone https://gitlab.inria.fr/scotch/scotch.git
```