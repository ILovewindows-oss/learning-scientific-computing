# -*- coding: utf-8 -*-

def compute_atomic_fraction(x_cor, x_cao):
    """ Compute atomic fractions to use in calculations. """
    total = 5 * x_cor + 2 * x_cao

    x_al = 2 * x_cor / total
    x_ca = 1 * x_cao / total

    print(f"*** COMPOUND C({x_cao}).A({x_cor})")
    print(f"SET CONDITION X(AL)={x_al:.5f}")
    print(f"SET CONDITION X(CA)={x_ca:.5f}")
    print("\n")


compute_atomic_fraction(0.0, 1.0)
compute_atomic_fraction(1.0, 3.0)
compute_atomic_fraction(1.0, 1.0)
compute_atomic_fraction(2.0, 1.0)
compute_atomic_fraction(6.0, 1.0)
compute_atomic_fraction(1.0, 0.0)

# Between CAO and C3A1
compute_atomic_fraction(0.9, 3.0)

# Between C3A1 and C1A1
compute_atomic_fraction(0.9, 1.0)

# Between C1A1 and C1A2
compute_atomic_fraction(2.0, 1.2)

# Between C1A2 and C1A6
compute_atomic_fraction(6.0, 1.02)

# Between C1A6 and COR
compute_atomic_fraction(1.0, 0.1)
