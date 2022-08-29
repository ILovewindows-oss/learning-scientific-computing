# Clean-up prior run.
Remove-Item -Force -Path solution.vtu
Remove-Item -Force -Path history.csv

# Run with 4 processors.
mpiexec -np 4 SU2_CFD case.cfg
