import numpy as np

from qmsolver.potentials import BasePotential
from qmsolver.tise.finite_differences import FDSolver


class SinusoidalWellPotential(BasePotential):
    """
    A composite sinusoidal potential with well and barrier regions:

        V(x) = A/2 + V_well(x) + V_barrier(x)

    where:
        - V_well(x)    = -A * |sin(x)| for      |x| ≤ π          , else 0
        - V_barrier(x) =  A * |sin(x)| for  π < |x| ≤ (5/6 + 2)π , else 0
        - A/2                          for      |x| > (5/6 + 2)π , else 0
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
        return (
            np.where(
                np.abs(self.x_grid) <= np.pi,
                -self.amplitude * np.abs(np.sin(self.x_grid)),
                0,
            )
            + np.where(
                (np.abs(self.x_grid) >= np.pi)
                & (np.abs(self.x_grid) <= (5 / 6 + 2) * np.pi),
                self.amplitude * np.abs(np.sin(self.x_grid)),
                0,
            )
            + np.where(
                np.abs(self.x_grid) >= (5 / 6 + 2) * np.pi,
                self.amplitude / 2,
                0,
            )
        )


solver = FDSolver(steps=2000, x_min=-4 * np.pi, x_max=4 * np.pi, n_lowest=15)
potential = SinusoidalWellPotential(x_grid=solver.x_grid, amplitude=5)
solver.potential_generator = potential
solver.solve()
solver.output()
solver.plot(save_path="outputs/sinusoidal_well.png")
