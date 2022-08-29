# -*- coding: utf-8 -*-
import json
import cantera as ct
import matplotlib.pyplot as plt
import numpy as np

T_min = 0.0
T_max = 100.0
num_states = 20

T = np.linspace(T_min, T_max, num_states) + 273.15
X = "CH4:1"

gas = ct.Solution("gri30.yaml", "gri30")

sol = ct.SolutionArray(gas, shape=(num_states,))
sol.TPX = T, ct.one_atm, X

TC = T - 273.15

p0 = np.polyfit(T, sol.viscosity, 2)
p1 = np.polyfit(T, sol.cp_mass, 2)
p2 = np.polyfit(T, sol.thermal_conductivity, 2)

v0 = np.polyval(p0, T)
v1 = np.polyval(p1, T)
v2 = np.polyval(p2, T)

props = {
    "viscosity": p0.tolist(),
    "cp_mass": p1.tolist(),
    "thermal_conductivity": p2.tolist()
}

with open("properties.json", "w") as fp:
    json.dump(props, fp, indent=4)

plt.close("all")
plt.style.use("seaborn-white")
plt.figure(figsize=(12, 4))

plt.subplot(131)
plt.plot(TC, sol.viscosity * 1e5, "ro")
plt.plot(TC, v0 * 1e5, "k:")
plt.title("f(T)={:+.3e}T²{:+.3e}T{:+.3e}".format(*p0))
plt.xlabel(r"Temperature [$^\circ{}C$]")
plt.ylabel(r"Viscosity [$10^5\times\mathrm{Pa\cdotp{}s}$]")
plt.grid(linestyle=":")
plt.xlim(T_min, T_max)

plt.subplot(132)
plt.plot(TC, sol.cp_mass, "ro")
plt.plot(TC, v1, "k:")
plt.title("f(T)={:+.3e}T²{:+.3e}T{:+.3e}".format(*p1))
plt.xlabel(r"Temperature [$^\circ{}C$]")
plt.ylabel(r"Heat capacity [$\mathrm{J\cdotp{}kg^{-1}\cdotp{}K^{-1}}$]")
plt.grid(linestyle=":")
plt.xlim(T_min, T_max)

plt.subplot(133)
plt.plot(TC, sol.thermal_conductivity, "ro")
plt.plot(TC, v2, "k:")
plt.title("f(T)={:+.3e}T²{:+.3e}T{:+.3e}".format(*p2))
plt.xlabel(r"Temperature [$^\circ{}C$]")
plt.ylabel(r"Thermal conductivity [$\mathrm{W\cdotp{}m^{-1}\cdotp{}K^{-1}}$]")
plt.grid(linestyle=":")
plt.xlim(T_min, T_max)

plt.tight_layout()
plt.savefig("properties.png", dpi=200)
