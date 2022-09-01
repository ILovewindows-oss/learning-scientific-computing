# -*- coding: utf-8 -*-
import numpy as np


TC: float = 647.096
""" Critical temperature [K]. """

RHOC: float = 322.0
""" Critical density [kg/m3]. """

R: float = 0.46151805
""" Specific gas constant [kJ/kg/K]. """


def f_helmholtz(rho: float, T: float, n0: list[float],
                gamma0: list[float]) -> float:
    """ Helmholtz free energy (4). """
    delta = rho / RHOC
    tau = TC / T

    phi0 = phi0_ideal_gas(delta, tau, n0, gamma0)
    phi_tau = phi_tau_residual(delta, tau)

    return R * T * (phi0 + phi_tau)


def phi0_ideal_gas(delta: float, tau: float, n0: list[float],
                   gamma0: list[float]) -> float:
    """ Ideal gas component of Helmholtz free energy. """
    phi0 = np.log(delta) + n0[1] + n0[2] * tau + n0[3] * np.log(tau)

    for k in range(4, 8+1):
        phi0 += n0[k] * np.log(1 - np.exp(-gamma0[k] * tau))

    return phi0


def phi_tau_residual(delta, tau):
    """ Residual part component of Helmholtz free energy. """
    return 0


table_01 = [
#   n                     gamma
    np.nan,               np.nan,           # 0
    -8.3204464837497e+00, np.nan,           # 1
    +6.6832105275932e+00, np.nan,           # 2
    +3.0063200000000e+00, np.nan,           # 3
    +0.0124360000000e+00, +1.28728967e+00,  # 4
    +0.9731500000000e+00, +3.53734222e+00,  # 5
    +1.2795000000000e+00, +7.74073708e+00,  # 6
    +0.9695600000000e+00, +9.24437796e+00,  # 7
    +0.2487300000000e+00, +2.75075105e+01   # 8
]

table_02 = [
#   c       d       t       n       alpha   beta    gamma   epsilon
    np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan,  # 0
    np.nan, 1,      -0.500, np.nan, np.nan, np.nan, np.nan, np.nan,  # 1
    np.nan, 1,      0.875,  np.nan, np.nan, np.nan, np.nan, np.nan,  # 2
    np.nan, 1,      1.000,  np.nan, np.nan, np.nan, np.nan, np.nan,  # 3
    np.nan, 2,      0.500,  np.nan, np.nan, np.nan, np.nan, np.nan,  # 4
    np.nan, 2,      0.750,  np.nan, np.nan, np.nan, np.nan, np.nan,  # 5
    np.nan, 3,      0.375,  np.nan, np.nan, np.nan, np.nan, np.nan,  # 6
    np.nan, 4,      1,      np.nan, np.nan, np.nan, np.nan, np.nan,  # 7
    1,      1,      4,      np.nan, np.nan, np.nan, np.nan, np.nan,  # 8
    1,      1,      6,      np.nan, np.nan, np.nan, np.nan, np.nan,  # 9

#   c       d       t       n       alpha   beta    gamma   epsilon
    1,      1,      12,     np.nan, np.nan, np.nan, np.nan, np.nan,  # 10
    1,      2,      1,      np.nan, np.nan, np.nan, np.nan, np.nan,  # 11
    1,      2,      5,      np.nan, np.nan, np.nan, np.nan, np.nan,  # 12
    1,      3,      4,      np.nan, np.nan, np.nan, np.nan, np.nan,  # 13
    1,      4,      2,      np.nan, np.nan, np.nan, np.nan, np.nan,  # 14
    1,      4,      13,     np.nan, np.nan, np.nan, np.nan, np.nan,  # 15
    1,      5,      9,      np.nan, np.nan, np.nan, np.nan, np.nan,  # 16
    1,      7,      3,      np.nan, np.nan, np.nan, np.nan, np.nan,  # 17
    1,      9,      4,      np.nan, np.nan, np.nan, np.nan, np.nan,  # 18
    1,      10,     11,     np.nan, np.nan, np.nan, np.nan, np.nan,  # 19

#   c       d       t       n       alpha   beta    gamma   epsilon
    1,      11,     4,      np.nan, np.nan, np.nan, np.nan, np.nan,  # 20
    1,      13,     13,     np.nan, np.nan, np.nan, np.nan, np.nan,  # 21
    1,      15,     1,      np.nan, np.nan, np.nan, np.nan, np.nan,  # 22
    2,      1,      7,      np.nan, np.nan, np.nan, np.nan, np.nan,  # 23
    2,      2,      1,      np.nan, np.nan, np.nan, np.nan, np.nan,  # 24
    2,      2,      9,      np.nan, np.nan, np.nan, np.nan, np.nan,  # 25
    2,      2,      10,     np.nan, np.nan, np.nan, np.nan, np.nan,  # 26
    2,      3,      10,     np.nan, np.nan, np.nan, np.nan, np.nan,  # 27
    2,      4,      3,      np.nan, np.nan, np.nan, np.nan, np.nan,  # 28
    2,      5,      7,      np.nan, np.nan, np.nan, np.nan, np.nan,  # 29

#   c       d       t       n       alpha   beta    gamma   epsilon
    2,      4,      10,     np.nan, np.nan, np.nan, np.nan, np.nan,  # 30
    2,      5,      10,     np.nan, np.nan, np.nan, np.nan, np.nan,  # 31
    2,      6,      6,      np.nan, np.nan, np.nan, np.nan, np.nan,  # 32
    2,      6,      10,     np.nan, np.nan, np.nan, np.nan, np.nan,  # 33
    2,      7,      10,     np.nan, np.nan, np.nan, np.nan, np.nan,  # 34
    2,      9,      1,      np.nan, np.nan, np.nan, np.nan, np.nan,  # 35
    2,      9,      2,      np.nan, np.nan, np.nan, np.nan, np.nan,  # 36
    2,      9,      3,      np.nan, np.nan, np.nan, np.nan, np.nan,  # 37
    1,      9,      4,      np.nan, np.nan, np.nan, np.nan, np.nan,  # 38
    1,      9,      8,      np.nan, np.nan, np.nan, np.nan, np.nan,  # 39

#   c       d       t       n       alpha   beta    gamma   epsilon
    2,      10,     6,      np.nan, np.nan, np.nan, np.nan, np.nan,  # 40
    2,      10,     9,      np.nan, np.nan, np.nan, np.nan, np.nan,  # 41
    2,      12,     8,      np.nan, np.nan, np.nan, np.nan, np.nan,  # 42
    3,      3,      16,     np.nan, np.nan, np.nan, np.nan, np.nan,  # 43
    3,      4,      22,     np.nan, np.nan, np.nan, np.nan, np.nan,  # 44
    3,      4,      23,     np.nan, np.nan, np.nan, np.nan, np.nan,  # 45
    3,      5,      23,     np.nan, np.nan, np.nan, np.nan, np.nan,  # 46
    4,      14,     10,     np.nan, np.nan, np.nan, np.nan, np.nan,  # 47
    6,      3,      50,     np.nan, np.nan, np.nan, np.nan, np.nan,  # 48
    6,      6,      44,     np.nan, np.nan, np.nan, np.nan, np.nan,  # 49

#   c       d       t       n       alpha   beta    gamma   epsilon
    6,      6,      46,     np.nan, np.nan, np.nan, np.nan, np.nan,  # 50
    6,      6,      50,     np.nan, np.nan, np.nan, np.nan, np.nan,  # 51
    np.nan, 3,      0,      np.nan, 20,     150,    1.21,   1,       # 52
    np.nan, 3,      1,      np.nan, 20,     150,    1.21,   1,       # 53
    np.nan, 3,      4,      np.nan, 20,     250,    1.25,   1,       # 54
    3.5,    0.85,   0.2,    np.nan, 28,     700,    0.32,   0.3,     # 55
    3.5,    0.95,   0.2,    np.nan, 32,     800,    0.32,   0.3      # 56
]

table_06 = []

# Tests
table_07 = []
table_08 = []