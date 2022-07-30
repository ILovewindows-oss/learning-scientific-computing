# -*- coding: utf-8 -*-
"""
Lennard-Jones Potential Fluid
=============================

This tutorial makes a summary of original implementation provided with
ESPResSo and keeps only relevant points from a copy-paste study session.
For details refer to `01-lennard_jones.ipynb` provided in the docs of the
software package. Several blocks were reorganized in a more reusable way.

The Lennard-Jones Potential
---------------------------

A pair  of  neutral  atoms  or  molecules  is  subject  to  two  distinct
forces  in  the  limit  of large separation and small separation:  an
attractive force at long ranges (van der Waals force, or dispersion force)
and a repulsive force at short ranges (the result of overlapping electron 
orbitals,  referred  to  as  Pauli  repulsion  from  the Pauli  exclusion
principle). The Lennard-Jones potential (also  referred  to  as  the  L-J
potential, 6-12 potential  or, less commonly, 12-6 potential) is a simple
mathematical model that represents this behavior. It  was  proposed  in 
1924  by  John  Lennard-Jones. The  L-J  potential  is  of  the  form

\begin{equation}
V(r) = 4\epsilon
\left[
    \left(\dfrac{\sigma}{r}\right)^{12} - 
    \left(\dfrac{\sigma}{r}\right)^{6}
\right]
\end{equation}

where $\epsilon$ is the depth of the potential well and $\sigma$ is the
(finite) distance at which the inter-particle potential is zero and $r$ is
the distance between the particles. The $\left(\frac{1}{r}\right)^{12}$ term
describes repulsion and the $(\frac{1}{r})^{6}$  term describes attraction.
The Lennard-Jones potential is an approximation. The form of the repulsion
term has no theoretical justification; the repulsion force should depend
exponentially on the distance, but the repulsion term of the L-J formula is
more convenient due to the ease and efficiency of computing $r^{12}$ as the
square of $r^6$.

In practice, the L-J potential is cutoff beyond a specified distance $r_{c}$
and the potential at the cutoff distance is zero.

Unit system
-----------

Novice users must understand that ESPResSo has no fixed unit system. The unit
system is set by the user. Conventionally, reduced units are employed, in
other words L-J units.

Organization of the simulation script
-------------------------------------

- System setup (box geometry, thermodynamic ensemble, integrator parameters)
- Placing (randomly) the particles in the system
- Setup of interactions between particles
- Warm up (bringing the system into a state suitable for measurements)
- Integration loop (propagate the system in time and record measurements)

Exercises: binary Lennard-Jones liquid
--------------------------------------

A two-component Lennard-Jones liquid can be simulated by placing particles of
two types (0 and 1) into the system. Depending on the Lennard-Jones parameters,
the two components either mix or separate.

1. Modify the code such that half of the particles are of <tt>type=1</tt>. 
   Type 0 is implied for the remaining particles.
2. Specify Lennard-Jones interactions between type 0 particles with other type
   0 particles, type 1 particles with other type 1 particles, and type 0
   particles with type 1 particles (set parameters for 
   <tt>system.non_bonded_inter[i,j].lennard_jones</tt> where <tt>{i,j}</tt>
   can be <tt>{0,0}</tt>, <tt>{1,1}</tt>, and <tt>{0,1}</tt>. Use the same
   Lennard-Jones parameters for interactions within a component, but use a
   different <tt>lj_cut_mixed</tt> parameter for the cutoff of the Lennard-Jones
   interaction between particles of type 0 and particles of type 1. Set this
   parameter to $2^{\frac{1}{6}}\sigma$ to get de-mixing or to $2.5\sigma$ to get
   mixing between the two components.
3. Record the radial distribution functions separately for particles of type 0
   around particles of type 0, type 1 around particles of type 1, and type 0
   around particles of type 1. This can be done by changing the
   <tt>type_list</tt> arguments of the <tt>system.analysis.rdf()</tt> command.
   You can record all three radial distribution functions in a single
   simulation. It is also possible to write them as several columns into a
   single file.
4. Plot the radial distribution functions for all three combinations of particle
   types. The mixed case will differ significantly, depending on your choice of
   <tt>lj_cut_mixed</tt>. Explain these differences.
"""
from IPython import embed
from espressomd.observables import ParticlePositions
from espressomd.accumulators import Correlator
import warnings
import numpy as np
import matplotlib.pyplot as plt
import espressomd

SEED = 42

MIN_WARMUP_STEP = 20

np.random.seed(SEED)


def check_features(required_features):
    """ Check if features are available. """
    try:
        espressomd.assert_features(required_features)
        return True
    except RuntimeError as err:
        print(f"When requiring {required_features} got {err}")
        print(f"Available features {espressomd.features()}")
    return False


def make_system_box(no_part, density, time_step):
    """ Create box system with given density of particles. 
    
    The density of particles being defined by the number of particles by
    the volume of the box, one can estimate the side of the containing
    box as :math:`l=\left(\frac{N}{\rho}\right)^(\frac{1}{3})`.
    """
    def side(N, rho):
        return (N / rho) ** (1 / 3)
    
    box_l = side(no_part, density) * np.ones(3)
    system = espressomd.System(box_l=box_l)
    system.seed = SEED
    system.time_step = time_step
    return system


def warmup_system(system, lj_cap, min_dist, n_steps=100, n_time_steps=1000):
    """ Perform system warm-up to avoid overlapping particles. """
    act_min_dist = system.analysis.min_dist()
    
    for k in range(n_time_steps):
        if not k % 100:
            print(f"Warm-up step .... {k}/{n_time_steps}")
        
        if k > MIN_WARMUP_STEP and act_min_dist < min_dist:
            print(f"Exit on {k}: {act_min_dist} < {min_dist}")
            break
            
        system.integrator.run(n_steps)
        act_min_dist = system.analysis.min_dist()

        lj_cap += 1.0
        system.force_cap = lj_cap

        
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    
    print("*** STARTING LENNARD-JONES FLUID SIMULATION")
    
    required_features = ["LENNARD_JONES"]
    if not check_features(required_features):
        raise Exception("Required features are not available.")
    
    ##########################################################################
    # SYSTEM SETUP
    ##########################################################################

    # Integration physical time step.
    time_step = 0.01
    
    # System temperature.
    kT = 0.728
    
    # Number of particles in system.
    no_part = 100

    # Occupation density of particles in system.
    density = 0.5

    # Make system.
    system = make_system_box(no_part, density, time_step)

    # skin?
    system.cell_system.skin = 0.4

    ##########################################################################
    # CHOOSING THE THERMODYNAMIC ENSEMBLE AND THERMOSTAT
    #
    # Availablem ensembles are NVE, NVT, and NPT-isotropic, with:
    # - N: number of particles
    # - V: volume
    # - E: energy
    # - T: temperature
    # - P: pressure
    #
    ##########################################################################

    # The NVE ensemble is simulated without a thermostat. A previously enabled
    # thermostat can be switched off as follows:
    system.thermostat.turn_off()

    # The NVT and NPT ensembles require a thermostat. In this tutorial, we
    # use the Langevin thermostat. Use a Langevin thermostat (NVT or NPT
    # ensemble) with temperature set and damping coefficient to gamma.
    system.thermostat.set_langevin(kT=kT, gamma=1.0, seed=SEED)

    ##########################################################################
    # PLACING AND ACCESSING PARTICLES
    ##########################################################################

    for k in range(no_part):
        pos = np.random.random(3) * system.box_l
        system.part.add(type=k % 2, pos=pos)

    # Access position of a single particle
    # print("position of particle with id 0:", system.part[0].pos)

    # Iterate over the first five particles for the purpose of demonstration.
    # For accessing all particles, use a slice: system.part[:]
    # for i in range(5):
    #     print("id", i, "position:", system.part[i].pos)
    #     print("id", i, "velocity:", system.part[i].v)

    # Inspect string representation of object.
    # print(system.part[0])
    
    # Obtain all particle positions
    # cur_pos = system.part[:].pos

    ##########################################################################
    # SETTING UP NON-BONDED INTERACTIONS
    #
    # Non-bonded interactions act between all particles of a given combination
    # of particle types. In this tutorial, we use the Lennard-Jones non-bonded
    # interaction. Set interaction of two particles of type 0:
    ##########################################################################
    
    LJ_EPS = 1.0
    LJ_SIG = 1.0
    LJ_CUT = 2.5 * LJ_SIG
    LJ_CAP = 0.5

    lj_cut_mixed = 2 ** (1/6) * LJ_SIG
    
    system.non_bonded_inter[0, 0].lennard_jones.set_params(
        epsilon=LJ_EPS, sigma=LJ_SIG, cutoff=LJ_CUT, shift="auto")
    system.non_bonded_inter[1, 1].lennard_jones.set_params(
        epsilon=LJ_EPS, sigma=LJ_SIG, cutoff=LJ_CUT, shift="auto")
    system.non_bonded_inter[0, 1].lennard_jones.set_params(
        epsilon=LJ_EPS, sigma=LJ_SIG, cutoff=lj_cut_mixed, shift="auto")

    system.force_cap = LJ_CAP

    ##########################################################################
    # WARMUP
    #
    # In many cases, including this tutorial, particles are initially placed
    # randomly in the simulation box. It is therefore possible that particles
    # overlap, resulting in a huge repulsive force between them. In this case,
    # integrating the equations of motion would not be numerically stable.
    # Hence, it is necessary to remove this overlap. This is done by limiting
    # the maximum force between two particles, integrating the equations of
    # motion, and increasing the force limit step by step as follows:
    ##########################################################################

    warmup_system(system, LJ_CAP, 0.87, n_steps=100, n_time_steps=2000)
    
    ##########################################################################
    # INTEGRATION AND MEASUREMENTS
    ##########################################################################
    
    # Force capping is switched off ater warmup by setting it to zero.
    system.force_cap = 0
    
    sampling_interval = 100
    sampling_iterations = 4000

    # Pass the ids of the particles to be tracked to the observable.
    part_pos = ParticlePositions(ids=range(no_part))

    # The mean square displacement of particle $i$ is given by:
    #
    # \begin{equation}
    # \mathrm{msd}_i(t) = \langle(\vec{x}_i(t_0+t) -\vec{x}_i(t_0))^2\rangle
    # \end{equation}
    #
    # and can be calculated using "observables and correlators". An observable
    # is an object which takes a measurement on the system. It can depend on
    # parameters specified when the observable is instanced, such as the ids
    # of the particles to be considered. Initialize MSD correlator.
    msd_corr = Correlator(obs1=part_pos,
                          tau_lin=10, delta_N=10,
                          tau_max=1000 * time_step,
                          corr_operation="square_distance_componentwise")

    # Calculate results automatically during the integration
    system.auto_update_accumulators.add(msd_corr)

    # Set parameters for the radial distribution function
    r_bins = 70
    r_min = 0.0
    r_max = system.box_l[0] / 2.0

    # Initialize 
    avg_rdf = np.zeros((r_bins, 3))
    time = np.zeros(sampling_iterations)
    temperature = np.zeros(sampling_iterations)
    etotal = np.zeros(sampling_iterations)
   
    opts = dict(r_min=r_min, r_max=r_max, r_bins=r_bins)
    
    # Loop over a given number of steps.
    for i in range(1, sampling_iterations + 1):
        if not i % 10:
            print(f"On run {i}/{sampling_iterations}")
        
        system.integrator.run(sampling_interval)
        
        # Measure radial distribution function
        r, rdf00 = system.analysis.rdf(rdf_type="rdf", type_list_a=[0],
                                       type_list_b=[0], **opts)
        r, rdf11 = system.analysis.rdf(rdf_type="rdf", type_list_a=[1],
                                       type_list_b=[1], **opts)
        r, rdf01 = system.analysis.rdf(rdf_type="rdf", type_list_a=[0],
                                       type_list_b=[1], **opts)
        avg_rdf[:, 0] += rdf00 / sampling_iterations
        avg_rdf[:, 1] += rdf11 / sampling_iterations
        avg_rdf[:, 2] += rdf01 / sampling_iterations

        # The potential and kinetic energies can be monitored using the
        # analysis method `system.analysis.energy()`. `kinetic_temperature`
        # refers to the measured temperature obtained from kinetic energy and
        # the number of degrees of freedom in the system. It should fluctuate
        # around the preset temperature of the thermostat.
        energies = system.analysis.energy()
        kinetic_temperature = (2 / 3) * energies["kinetic"] / no_part

        temperature[i - 1] = kinetic_temperature
        etotal[i - 1] = energies["total"]
        time[i - 1] = system.time

    # Finalize the correlator and obtain the results. The first column of this
    # array contains the lag time in units of the time step. The second column
    # contains the number of values used to perform the averaging of the 
    # correlation. The next three columns contain the x, y and z mean squared
    # displacement of the msd of the first particle. The next three columns
    # then contain the x, y, z mean squared displacement of the next particle...
    msd_corr.finalize()
    msd = msd_corr.result()

    # Simple Error Estimation on Time Series Data. A simple way to estimate
    # the error of an observable is to use the standard error of the mean (SE)
    # for $N$ uncorrelated samples:
    #
    # \begin{equation}
    # SE = \sqrt{\frac{\sigma^2}{N}},
    # \end{equation}
    #
    # where $\sigma^2$ is the variance
    #
    # \begin{equation}
    # \sigma^2  = \left\langle x^2 - \langle x\rangle^2 \right\rangle
    # \end{equation}
    standard_error_total_energy = np.sqrt(etotal.var() / sampling_iterations)
    print("STD(Energy) = ", standard_error_total_energy)

    ##########################################################################
    # PLOT RESULTS
    ##########################################################################
    
    # We first plot the radial distribution function which describes how the
    # density varies as a function of distance from a tagged particle. The
    # radial distribution function is averaged over several measurements to
    # reduce noise.
    plt.close("all")
    plt.style.use("seaborn-white")
    plt.figure(figsize=(6, 6))
    plt.plot(r, avg_rdf[:, 0], "-", label="[0-0]")
    plt.plot(r, avg_rdf[:, 1], "-", label="[1-1]")
    plt.plot(r, avg_rdf[:, 2], "-", label="[0-1]")
    plt.grid(linestyle=":")
    plt.xlabel("r $[\sigma]$")
    plt.ylabel("$g(r)$")
    plt.legend()
    plt.tight_layout()
    plt.savefig("results/001-02-radial-function", dpi=300)
    
    plt.close("all")
    plt.style.use("seaborn-white")
    plt.figure(figsize=(6, 6))
    plt.plot(time, temperature, "r-", label="Instantaneous")
    plt.axhline(kT, color="k", linestyle=":")
    plt.grid(linestyle=":")
    plt.xlabel(r"Time [$\delta t$]", fontsize=20)
    plt.ylabel(r"$k_B$ Temperature [$k_B T$]", fontsize=20)
    plt.legend()
    plt.tight_layout()
    plt.savefig("results/001-02-temperature", dpi=300)

    plt.close("all")
    plt.style.use("seaborn-white")
    plt.figure(figsize=(6, 6))
    
    lag_time = msd[:, 0]
    for i in range(0, no_part, 30):
        k = 3 * i
        msd_particle_i = msd[:, 2 + k] + msd[:, 3 + k] + msd[:, 4 + k]
        plt.plot(lag_time, msd_particle_i, "o-", label=f"Particle {i:03}")

    plt.xlabel(r"Lag time $\tau$ [$\delta t$]", fontsize=20)
    plt.ylabel(r"Mean squared displacement [$\sigma^2$]", fontsize=20)
    plt.xscale("log")
    plt.yscale("log")
    plt.legend()
    plt.savefig("results/001-02-particle-msd", dpi=300)
    
    embed(colors="Linux")
