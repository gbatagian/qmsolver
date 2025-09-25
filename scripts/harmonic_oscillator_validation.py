import numpy as np
from scipy import constants

from qmsolver.potentials import HarmonicOscillatorPotential
from qmsolver.tise import FDSolver

x_min_m = -10e-9
x_max_m = 10e-9

solver = FDSolver(steps=10_000, x_min=x_min_m, x_max=x_max_m, n_lowest=5)

# Set physical constants in SI units
solver.h_bar = constants.hbar
solver.m = constants.m_e

# Create harmonic oscillator potential active over entire grid
omega = 1e14  # Angular frequency (rad/s)
m = constants.m_e
potential = HarmonicOscillatorPotential(
    x_grid=solver.x_grid,
    spring_constant=m * omega**2,
    grid_active_range=1,  # Active over entire grid
)
solver.potential_generator = potential

solver.solve()
solver.output()

E_lowest_ev = np.array(solver.E_lowest) / constants.e
print("\nEnergies in electron volts:")
s = 0
for i, energy in enumerate(E_lowest_ev):
    analytical_energy = (constants.hbar * omega * (i + 0.5)) / constants.e
    renormalized_energy = (
        energy + np.abs(np.min(solver.potential)) / constants.e
    )
    error = (
        100 * abs(renormalized_energy - analytical_energy) / analytical_energy
    )
    s += error
    print(
        f"E({i}) = {renormalized_energy:.8f} eV | E_HO({i}): {analytical_energy:.8f} eV | Error: {error:.8f} %"
    )

print(f"\nAverage error: {s/len(E_lowest_ev):.8f} %")
