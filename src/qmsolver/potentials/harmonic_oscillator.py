import numpy as np

from .base import BasePotential


class HarmonicOscillatorPotential(BasePotential):
    def __init__(
        self,
        x_grid: np.array,
        spring_constant: float,
        mass: float = 1.0,
        grid_active_range: float = 0.5,
    ):
        """
        Harmonic oscillator potential: V(x) = 0.5 * k * x^2

        Parameters:
        - x_grid (np.array): Spatial grid points
        - spring_constant (float): Spring constant k (or can use frequency via k = m*ω^2)
        - mass (float): Particle mass (default 1.0 for dimensionless units)
        """
        self.x_grid = x_grid
        self.spring_constant = spring_constant
        self.mass = mass
        self.grid_active_range = grid_active_range

    def generate(self) -> np.array:
        """
        Generate the harmonic oscillator potential array.

        Returns:
            np.array: Array of potential values, 0.5 * k * x^2.
        """
        right_limit = self.x_grid[-1]
        left_limit = self.x_grid[0]

        # Calculate the active range around the center of the grid
        center = (left_limit + right_limit) / 2
        half_active_range = (
            abs(right_limit - left_limit) * self.grid_active_range
        ) / 2

        ho_potential = np.where(
            (self.x_grid >= center - half_active_range)
            & (self.x_grid <= center + half_active_range),
            0.5 * self.spring_constant * (self.x_grid - center) ** 2,
            0,
        )

        # shift potential to have max at 0 (negative-well-like)
        shifted_ho_potential = np.where(
            ho_potential != 0, ho_potential - np.max(ho_potential), 0
        )

        return shifted_ho_potential

    @classmethod
    def from_frequency(
        cls, x_grid: np.array, frequency: float, mass: float = 1.0
    ):
        """
        Create harmonic oscillator potential from frequency ω.
        V(x) = 0.5 * m * ω^2 * x^2

        Parameters:
        - x_grid (np.array): Spatial grid points
        - frequency (float): Angular frequency ω
        - mass (float): Particle mass (default 1.0 for dimensionless units)

        Returns:
            HarmonicOscillatorPotential: Instance with appropriate spring constant
        """
        spring_constant = mass * frequency**2
        return cls(x_grid, spring_constant, mass)
