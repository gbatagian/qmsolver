import numpy as np
from scipy import constants

from qmsolver.potentials import FiniteSquareWellPotential
from qmsolver.tise import FDSolver

well_depth_ev = 1.0  # Well depth in electron volts
well_width_nm = 1.0  # Well width in nanometers

# Convert to SI units
well_depth_joules = well_depth_ev * constants.e  # Convert eV to Joules
well_width_meters = well_width_nm * 1e-9  # Convert nm to meters

# Spatial domain in meters
x_min_m = -3e-9
x_max_m = 3e-9

solver = FDSolver(steps=2_000, x_min=x_min_m, x_max=x_max_m, n_lowest=3)

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
solver.plot(
    is_dimensionless=False,
    scale=1e19,
    energy_units="J",
    save_path="outputs/finite_square_well_SI_units.png",
)

E_lowest_ev = np.array(solver.E_lowest) / constants.e
print("\nEnergies in electron volts:")
for i, energy in enumerate(E_lowest_ev):
    print(f"E({i}) = {energy:.8f} eV")
