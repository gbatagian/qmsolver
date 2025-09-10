import numpy as np

from qmsolver.potentials import BasePotential
from qmsolver.tise.finite_differences import FDSolver


class SinusoidalWellPotential(BasePotential):
    """
    A sinusoidal potential well: V(x) = -A * |sin(x)| for |x| ≤ π, 0 otherwise
    """

    def __init__(self, x_grid: np.array, amplitude: float) -> None:
        """
        Parameters:
        - x_grid: Spatial grid points
        - amplitude: Amplitude of the sinusoidal modulation (A > 0)
        """
        self.x_grid = x_grid
        self.amplitude = amplitude

    def generate(self) -> np.array:
        """
        Generate the potential energy array.

        Returns:
            np.array: Potential energy values on the grid
        """
        return np.where(
            np.abs(self.x_grid) <= np.pi,
            -self.amplitude * np.abs(np.sin(self.x_grid)),
            0.0,
        )


solver = FDSolver(steps=2000, x_min=-10, x_max=10, n_lowest=5)
potential = SinusoidalWellPotential(x_grid=solver.x_grid, amplitude=5.0)
solver.potential_generator = potential
solver.solve()
solver.output()
solver.plot(save_path="outputs/sinusoidal_well.png")
