# -*- coding: utf-8 -*-
from majordome.simulate.combustion import CombustorPSR
import matplotlib.pyplot as plt


def get_chemistry_set(fuel_sel, oxid_sel):
    """ Selector for experimenting with different compositions. """
    fuel = _select_fuel(fuel_sel)
    oxid = _select_oxid(oxid_sel)
    return fuel, oxid


def test_gri30(mech, phi, fuel, oxid, tau_max):
    """ Evaluate combustor for Gri-Mech 3.0. """
    mech = "gri30.yaml"
    spec = []
    comb = _test_excluding_species(mech, phi, fuel, oxid, tau_max, spec)
    return comb


def test_lu30_gri30(mech, phi, fuel, oxid, tau_max):
    """ Evaluate combustor for Lu mechanism with 30 species. """
    mech = "Lu_2008_CH4_sk30/lu30_gri30.cti"
    spec = ["C3H8"]
    comb = _test_excluding_species(mech, phi, fuel, oxid, tau_max, spec)
    return comb


def test_zhukov23_gri30(mech, phi, fuel, oxid, tau_max):
    """ Evaluate combustor for Zhukov mechanism with 23 species. """
    mech = "Zhukov_2018_sk23/zhukov23_gri30.cti"
    spec = ["C3H8"]
    comb = _test_excluding_species(mech, phi, fuel, oxid, tau_max, spec)
    return comb


def test_2s_ch4_bfer(mech, phi, fuel, oxid, tau_max):
    """ Evaluate combustor for low order mechanism 2 reactions. """
    mech = "Methane_Low_Order/2S_CH4_BFER.cti"
    spec = ["C2H6", "C3H8"]
    comb = _test_excluding_species(mech, phi, fuel, oxid, tau_max, spec)
    return comb


def _select_fuel(fuel_sel):
    """ Selector for fuel composition. """
    match fuel_sel:
        case "pure_methane":
            fuel = {
                "CH4":  1.0000
            }
        case "natural_gas_basic":
            fuel = {
                "CH4":  0.9500,
                "CO2":  0.0100,
                "N2":   0.0400
            }
        case "natural_gas_real":
            fuel = {
                "CH4":  0.9219,
                "C2H6": 0.0427,
                "C3H8": 0.0064,
                "CO2":  0.0095,
                "N2":   0.0195
            }
        case _:
            print(f"Unknown {fuel_sel}, getting pure methane")
            fuel = _select_fuel("pure_methane")

    return fuel


def _select_oxid(oxid_sel):
    """ Selector for oxidizer composition. """
    match oxid_sel:
        case "pure_oxygen":
            oxid = {
                "O2":   1.0000
            }
        case "pure_oxygen_humid":
            oxid = {
                "O2":   0.9950,
                "H2O":  0.0050
            }
        case "air":
            oxid = {
                "N2":   0.7800,
                "O2":   0.2100,
                "H2O":  0.0050
            }
        case _:
            print(f"Unknown {oxid_sel}, getting pure oxygen")
            oxid = _select_oxid("pure_oxygen")

    return oxid


def _test_mechanism(mech, phi, fuel, oxid, tau_max):
    """ Standardize reporting of mechanism tests. """
    tau_min = 0.0001 * tau_max
    comb = CombustorPSR(mech)
    comb.set_states(phi, fuel, oxid, basis="mole")
    comb.to_steady_state(tau_max, tau_min=tau_min, tau_dec=0.8)
    comb.plot(
        tau_scale=1000,
        xlim=(tau_min * 1000, tau_max * 1000),
        ax1_ylim=(1e+01, 1e+06),
        ax2_ylim=(1e-07, 1e+00),
        ax3_ylim=(0, 4000),
        loc=1
    )
    plt.show()
    return comb


def _test_excluding_species(mech, phi, fuel, oxid, tau_max, spec_list=[]):
    """ Manage species for mechanisms missing some of them. """
    fuel_local = {**fuel}

    for spec in spec_list:
        if spec in fuel_local:
            del fuel_local[spec]

    comb = _test_mechanism(mech, phi, fuel_local, oxid, tau_max)
    return comb
