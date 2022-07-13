# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt

# Alias to allow copying directly from TDB.
LN = np.log

# Temperature range to evaluate.
T = np.linspace(500, 3500, 1000)

condlist_quartz = [
    (T > 298.15)  & (T <= 540.00),
    (T > 540.00)  & (T <= 770.00),
    (T > 770.00)  & (T <= 848.00),
    (T > 848.00)  & (T <= 1800.00),
    (T > 1800.00) & (T <= 2960.00),
    (T > 2960.00)
]
funclist_quartz = [
    lambda T: -9.00936640e+05*T**0 -3.60892175e+02*T**1 +6.11323000e+01*T*LN(T) \
              -1.89203605e-01*T**2 +4.95097420e-05*T**3 -8.54401000e+05*T**(-1),
    lambda T: -1.09146654e+06*T**0 +2.88267275e+03*T**1 -4.52136700e+02*T*LN(T) \
              +4.28883845e-01*T**2 -9.09177060e-05*T**3 +1.24766890e+07*T**(-1),
    lambda T: -1.56348144e+06*T**0 +9.17858655e+03*T**1 -1.40453520e+03*T*LN(T) \
              +1.28406426e+00*T**2 -2.35047657e-04*T**3 +5.64023040e+07*T**(-1),
    lambda T: -9.28732923e+05*T**0 +3.56218325e+02*T**1 -5.84292000e+01*T*LN(T) \
              -5.15995000e-03*T**2 -2.47000000e-10*T**3 -9.51130000e+04*T**(-1),
    lambda T: -9.24076574e+05*T**0 +2.81229013e+02*T**1 -4.74510000e+01*T*LN(T) \
              -1.20031510e-02*T**2 +6.78127000e-07*T**3 +6.65385000e+05*T**(-1),
    lambda T: -9.57997400e+05*T**0 +5.44992084e+02*T**1 -8.27090000e+01*T*LN(T)
              +0.00000000e+00*T**2 +0.00000000e+00*T**3 +0.00000000e+00*T**(-1)
]

condlist_tridym = [
    (T > 900.00)  & (T <= 1668.00),
    (T > 1668.00) & (T <= 1800.00)
]
funclist_tridym = [
    lambda T: -5.06647740e+04*T**0 +4.92091478e+02*T**1 -7.00048000e+01*T*LN(T) \
              +3.90305000e-02*T**2 -3.78663600e-06*T**3 +7.16591300e+06*T**(-1),
    lambda T: -1.49543410e+04*T**0 +1.37362028e+02*T**1 -1.91583000e+01*T*LN(T) \
              +8.20019500e-03*T**2 -4.62871000e-07*T**3 +2.32223800e+06*T**(-1)
]

condlist_cristo = [
    (T > 848.00)  & (T <= 1800.00),
    (T > 1800.00) & (T <= 2960.00)
]
funclist_cristo = [
    lambda T: -1.43940000e+04*T**0 +1.37042236e+02*T**1 -1.91583000e+01*T*LN(T) \
              +8.20015900e-03*T**2 -4.62871000e-07*T**3 +2.32223800e+06*T**(-1),
    lambda T: -1.90509400e+04*T**0 +2.12031548e+02*T**1 -3.01365000e+01*T*LN(T) \
              +1.50433950e-02*T**2 -1.14126500e-06*T**3 +1.56174000e+06*T**(-1)
]

g_quartz = np.piecewise(T, condlist_quartz, funclist_quartz) / 1.0e+06
g_tridym = np.piecewise(T, condlist_tridym, funclist_tridym) / 1.0e+06
g_cristo = np.piecewise(T, condlist_cristo, funclist_cristo) / 1.0e+06

g_tridym += g_quartz
g_cristo += g_quartz

plt.close("all")
plt.style.use("seaborn-white")
plt.plot(T, g_quartz, label="Quartz")
plt.plot(T, g_tridym, label="Tridymite")
plt.plot(T, g_cristo, label="Cristobalite")
plt.grid(linestyle=":")
plt.xlabel("Temperature [K]")
plt.ylabel("G [J/mol]")
plt.legend()
plt.show()