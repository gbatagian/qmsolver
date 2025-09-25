import numpy as np
from scipy import constants

from qmsolver.potentials import FiniteSquareWellPotential
from qmsolver.tise import FDSolver

well_depth_ev = 1e12  # Well depth in electron volts
well_width_nm = 1.0  # Well width in nanometers

# Convert to SI units
well_depth_joules = well_depth_ev * constants.e  # Convert eV to Joules
well_width_meters = well_width_nm * 1e-9  # Convert nm to meters

# Spatial domain in meters
x_min_m = -3e-9
x_max_m = 3e-9

solver = FDSolver(steps=10_000, x_min=x_min_m, x_max=x_max_m, n_lowest=5)

# Set physical constants in SI units
solver.h_bar = constants.hbar  # Reduced Planck's constant in J⋅s
solver.m = constants.m_e  # Electron mass in kg

potential = FiniteSquareWellPotential(
    x_grid=solver.x_grid,
    well_depth=well_depth_joules,
    well_width=well_width_meters,
)
solver.potential_generator = potential

solver.solve()
solver.output()

E_lowest_ev = np.array(solver.E_lowest) / constants.e
print("\nEnergies in electron volts:")
for i, energy in enumerate(E_lowest_ev):
    infinite_square_Well_energy = (
        (i + 1) ** 2
        * constants.hbar**2
        * np.pi**2
        / (2 * solver.m * well_width_meters**2)
    ) / constants.e

    renormalized_energy = energy + well_depth_ev

    error = (
        100
        * abs(renormalized_energy - infinite_square_Well_energy)
        / infinite_square_Well_energy
    )

    print(
        f"E({i}) = {renormalized_energy:.8f} eV | E_ISW({i}): {infinite_square_Well_energy:.8f} eV | Error: {error:.8f} %"
    )
