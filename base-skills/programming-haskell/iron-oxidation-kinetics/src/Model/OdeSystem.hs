module Model.OdeSystem (rhs) where

import Typing (Nb)
import Model.Thermophysical (eps, cp)

-- Right-hand side of system of ODE's.
rhs :: Nb -> Nb -> Nb -> Nb -> Nb -> Nb -> Nb -> (Nb, Nb)
rhs t tk tw l h tc tm = (tmpDot t tk tw l h tc tm, tauDot t tk)

-- Time derivative of strip temperature.
tmpDot :: Nb -> Nb -> Nb -> Nb -> Nb -> Nb -> Nb -> Nb
tmpDot t tk tw l h tc tm = 2 * (rad + con) / (rhoSteel * l * cp tk)
    where rad   = sigma * (alpha * tw^4 - gamma * tk^4)
          con   = h * (tw - tk)
          alpha = eps t tw tc tm
          gamma = eps t tk tc tm

-- Time derivative of oxide thickness.
tauDot :: Nb -> Nb -> Nb
tauDot t tk = (kModel / t) * exp (-actEnergy / (gasConstant * tk))

-- Problem constant coefficient [m^2/s].
kModel :: Nb
kModel = (rhoSteel / rhoOxide) * (mwOxide / mwSteel) * diffZero

-- Stefan-Boltzmann constant [W/(m^2.K^4)].
sigma :: Nb
sigma = 5.670374419e-08

-- Ideal gas constant [J/(mol.K)].
gasConstant :: Nb
gasConstant = 8.31446261815324

-- Activation energy for diffusion in oxide [J/(mol.K)].
actEnergy :: Nb
actEnergy =  230000

-- Specific mass of magnetite [kg/m^3].
rhoOxide :: Nb
rhoOxide = 7874

-- Specific mass of steel [kg/m^3].
rhoSteel :: Nb
rhoSteel = 7890

-- Molar mass of magnetite [kg/mol].
mwOxide :: Nb
mwOxide = 0.231533

-- Molar mass of steel [kg/mol].
mwSteel :: Nb
mwSteel = 0.055845

-- Pre-exponential diffusivity coefficient [m^2/s].
diffZero :: Nb
diffZero = 0.00052
