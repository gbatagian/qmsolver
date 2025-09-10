from qmsolver.potentials import FiniteSquareWellPotential
from qmsolver.tise import FDSolver

solver = FDSolver(steps=2_000, x_min=-5, x_max=5, n_lowest=7)
potential = FiniteSquareWellPotential(
    x_grid=solver.x_grid, well_depth=25, well_width=2
)
solver.potential_generator = potential
solver.solve()
solver.output()
solver.plot(save_path="outputs/finite_square_well.png")
