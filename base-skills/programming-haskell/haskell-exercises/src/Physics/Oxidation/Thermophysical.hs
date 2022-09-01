module Physics.Oxidation.Thermophysical (eps, cp) where

import Physics.Typing (Nb)

-- Temperature and thickness dependent emissivity model.
eps :: Nb -> Nb -> Nb -> Nb -> Nb
eps t tk tc tm = p * epsSteel + (1 - p) * epsOxide
    where p = exp (-(t / tc) ** tm)
          epsSteel = epsModel tk epsParsSteel
          epsOxide = epsModel tk epsParsOxide
          epsModel tk' (a, b) = a * (1 - exp (-tk' / b))

-- Steel heat capacity [J/(kg.K)].
cp :: Nb -> Nb
cp tk = tk * (tk * (tk * (e * tk + d) + c) + b) + a
    where (a, b, c, d, e) = if tk < 1123 then cpParsL else cpParsH

-- Oxide emissivity parameters for temperature dependency.
epsParsOxide :: (Nb, Nb)
epsParsOxide = (9.35083100e-01, 5.1228971691e+02)

-- Steel emissivity parameters for temperature dependency.
epsParsSteel :: (Nb, Nb)
epsParsSteel = (3.08938352e-01, 8.4004408700e+02)

-- Low temperature range heat capacity coefficients.
cpParsL :: (Nb, Nb, Nb, Nb, Nb)
cpParsL = (7.726812135693e+02, -3.061763527505e+00,
           9.713590095324e-03, -1.177081491234e-05,
           5.368288667701e-09)

-- High temperature range heat capacity coefficients.
cpParsH :: (Nb, Nb, Nb, Nb, Nb)
cpParsH = (5.830451419897e+02, -1.943420512064e-01,
           2.581569711817e-04, -6.320141833273e-08,
           1.932134676071e-13)
