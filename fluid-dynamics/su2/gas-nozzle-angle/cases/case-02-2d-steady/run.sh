# Clean-up prior run.
rm -rf history*.csv
rm -rf restart*.dat
rm -rf solution*.vtu

# Run with 4 processors.
mpiexec -np 40 SU2_CFD case.cfg

# kill -9 $(ps ax | grep SU2 | cut -d " " -f3)
