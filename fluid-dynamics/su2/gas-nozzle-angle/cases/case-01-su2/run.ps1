# Clean-up prior run.
Remove-Item -Force -Path history*.csv
Remove-Item -Force -Path restart*.dat
Remove-Item -Force -Path solution*.vtu

# Run with 4 processors.
mpiexec -np 4 SU2_CFD case.cfg
