# -*- coding: utf-8 -*-
import warnings
import maicos
import matplotlib.pyplot as plt
import MDAnalysis as mda

warnings.simplefilter("ignore")

dump = "dumps/step-4-dynamics.lammpstrj"
u = mda.Universe(dump, topology_format="LAMMPSDUMP")

grp_Na = u.select_atoms("type 3")
grp_Cl = u.select_atoms("type 4")

dplanNa = maicos.DensityPlanar(grp_Na)
dplanCl = maicos.DensityPlanar(grp_Cl)

dplanNa.run()
dplanCl.run()

zcoorNa = dplanNa.results["z"]
zcoorCl = dplanCl.results["z"]

densNa = dplanNa.results["dens_mean"]
densCl = dplanCl.results["dens_mean"]

plt.close("all")
plt.style.use("seaborn-white")
plt.plot(zcoorCl, densCl, label="Cl$^-$")
plt.plot(zcoorNa, densNa, label="Na$^+$")
plt.grid(linestyle=":")
plt.xlabel("Coordinate z [Å]")
plt.ylabel("Density")
plt.legend(loc=1)
plt.tight_layout()
plt.show()
