# QMSolver

**QMSolver** is a Python library for numerically solving the time-independent Schrödinger equation in one dimension. The library implements the finite differences method to compute energy eigenvalues and eigenfunctions for quantum mechanical systems with arbitrary potential energy functions.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Method Limitations](#method-limitations)
- [Custom Potential Implementation](#custom-potential-implementation)
- [SI Units](#si-units)
- [Results Validation](#results-validation)
  - [Infinite Square Well Limit](#infinite-square-well-limit)
  - [Harmonic Oscillator Validation](#harmonic-oscillator-validation)
- [Development and Contributing](#development-and-contributing)
- [License](#license)
- [References](#references)

## Installation

### PyPI Installation

```bash
pip install qmsolver
```
**Requirements:** Python >= 3.9

### Repo Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/gbatagian/qmsolver.git
   cd qmsolver
   ```

2. **Install the source code:**
   ```bash
   pip install -e .
   ```

## Usage

### Finite Differences Solver (`FDSolver`)

The `qmsolver` package provides the `tise` module, which contains the `FDSolver` class for solving the time-independent Schrödinger equation using finite differences. To use it, create an `FDSolver` instance and inject a potential class into its `potential_generator` attribute. Sample potentials are provided in the `potentials` module. For example, the finite square well solution is demonstrated below:

```python
from qmsolver.tise import FDSolver
from qmsolver.potentials import FiniteSquareWellPotential

solver = FDSolver(steps=2_000, x_min=-5, x_max=5, n_lowest=7)
potential = FiniteSquareWellPotential(
    x_grid=solver.x_grid, well_depth=25, well_width=2
)
solver.potential_generator = potential
solver.solve()
solver.output()
solver.plot()
```

```bash
****************************************

-> 7 lowest energy states:

      🔒   E(0)  =  -24.0554383661  (bound)
      🔒   E(1)  =  -21.2408973698  (bound)
      🔒   E(2)  =  -16.6240464549  (bound)
      🔒   E(3)  =  -10.3701336891  (bound)
      🔒   E(4)  =   -2.9999825644  (bound)
      🌊   E(5)  =    0.2854054853  (free) 
      🌊   E(6)  =    0.3280462337  (free) 

****************************************
```

> **⚠️ Attention:** The `FiniteSquareWellPotential` class requires a spatial grid as input. It is recommended to provide the `x_grid` of the solver to ensure the potential and solver use the same grid.

This will generate a plot showing the potential (black line) and the first few bound eigenstates:


![Finite Square Well Example](outputs/finite_square_well.png)

> **Note:** The `plot()` method only displays **bound states** (i.e. $E < V_{asymptotic}$, where $V_{asymptotic}$ is the min value at the boundaries), as these are the physically meaningful solutions under the finite differences method. Free states are affected by the zero boundary conditions which result grid-dependent "artificial quantization" of the continuum energy spectrum. For more information, see the [Method Limitations](#method-limitations) section

> **Note:** You can customize the physical constants by setting the `solver.h_bar` and `solver.m` attributes to your desired values before calling `solver.solve()`. By default, they are set to 1 (dimensionless units). For more information on using SI units, see the [SI Units](#si-units) section.

* After calling `solver.solve()`, the solver will have the `E_lowest` attribute containing the n-lowest eigenenergies and the `Psi_lowest` attribute containing the corresponding eigenfunctions.
    ```python
    solver.E_lowest
    ```
    ```bash
    array([-24.05543837, -21.24089737, -16.62404645, -10.37013369, -2.99998256, 0.28540549])
    ```

    ```python
    solver.Psi_lowest 
    ```
    ```bash
    array([[ 7.72546314e-16, -7.70210475e-15,  2.04525254e-13,
            2.68267151e-11,  7.52877452e-08,  1.30754252e-04],
        [ 1.54602276e-15, -1.54123977e-14,  4.09220681e-13,
            5.36673540e-11,  1.50586795e-07,  2.61506636e-04],
        [ 2.32136057e-15, -2.31390756e-14,  6.14256593e-13,
            8.05358477e-11,  2.25908455e-07,  3.92255285e-04],
        ...,
        [ 2.32136057e-15,  2.31390756e-14,  6.14256593e-13,
            -8.05358477e-11,  2.25908455e-07, -3.92255285e-04],
        [ 1.54602276e-15,  1.54123977e-14,  4.09220681e-13,
            -5.36673540e-11,  1.50586795e-07, -2.61506636e-04],
        [ 7.72546314e-16,  7.70210475e-15,  2.04525254e-13,
            -2.68267151e-11,  7.52877452e-08, -1.30754252e-04]],
        shape=(2000, 6))
    ```

* Additionally, the solver provides `E_bound` and `Psi_bound` attributes containing only the bound states:
    ```python
    solver.E_bound
    ```
    ```bash
    array([-24.05543837, -21.24089737, -16.62404645, -10.37013369, -2.99998256])
    ```

    ```python
    solver.Psi_bound
    ```
    ```bash
    array([[ 7.72546314e-16, -7.70210475e-15,  2.04525254e-13,
             2.68267151e-11,  7.52877452e-08],
        [ 1.54602276e-15, -1.54123977e-14,  4.09220681e-13,
             5.36673540e-11,  1.50586795e-07],
        [ 2.32136057e-15, -2.31390756e-14,  6.14256593e-13,
             8.05358477e-11,  2.25908455e-07],
        ...,
        [ 2.32136057e-15,  2.31390756e-14,  6.14256593e-13,
            -8.05358477e-11,  2.25908455e-07],
        [ 1.54602276e-15,  1.54123977e-14,  4.09220681e-13,
            -5.36673540e-11,  1.50586795e-07],
        [ 7.72546314e-16,  7.70210475e-15,  2.04525254e-13,
            -2.68267151e-11,  7.52877452e-08]], shape=(2000, 5))
    ```
## Method Limitations

The finite difference method is well-suited for computing **bound states** of quantum systems, but has some limitations for **free states** (scattering or continuum states).

The numerical implementation imposes **zero boundary conditions** at the edges of the spatial grid (**x_min** and **x_max**). This effectively encloses the system within an **infinite square well** of width (x_max - x_min), which introduces artificial quantization of the continuum energy spectrum.

For bound states, the wavefunctions decay exponentially to zero outside the well region. Since they naturally satisfy the zero boundary conditions at the grid edges, the computed energies and wave functions are unaffected by the grid size, provided the grid extends sufficiently far to capture the exponential decaying tail.

For free states, the wavefunctions oscillate and do not decay to zero. The artificial boundary conditions at the grid edges cause **reflection** of the wavefunction, creating standing waves that depend on the grid length. This leads to:
  - **Quantization** of the continuum spectrum
  - **Grid-dependent** energy levels and wavefunctions

`FDSolver` is better-suited for bound state problems and provides reliable results within that domain - as long as the grid extends sufficiently beyond the potential region to minimize boundary effects. For free states, the numerical solutions behave as if the system is confined within an infinite potential well, with complete wavefunction reflection at the grid boundaries, leading to quantization of the continuum energy spectrum. 

## Custom Potential Implementation

While the `potentials` module provides several predefined potential classes, you can also implement custom potentials by inheriting from the `BasePotential` abstract base class. This allows you to solve the Schrödinger equation for arbitrary potential energy functions. To create a custom potential class:

1. **Inherit from `BasePotential`**: Your class must inherit from `potentials.base.BasePotential`
2. **Implement the `generate()` method**: This method should return a NumPy array containing the potential energy values evaluated on the spatial grid
3. **Accept grid as input**: The `__init__` method should accept the spatial grid (`x_grid`) as a parameter
4. **Instance attribute parameters**: Any potential parameters (depths, widths, etc.) should be stored as instance attributes

Below follows an example implementation of a sinusoidal potential well:

> **⚠️ Important:** All parameters required by the `generate()` method must be provided through the `__init__` method and stored as instance attributes (accessed through the `self` namespace). The `generate()` method should not accept additional parameters - it should only return the potential array using the stored parameters and the grid.

```python
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
solver.plot()

```

```bash
****************************************

-> 15 lowest energy states:

      🔒   E(0)  =   -3.9318637166  (bound)
      🔒   E(1)  =   -3.9000190100  (bound)
      🔒   E(2)  =   -1.9641284920  (bound)
      🔒   E(3)  =   -1.6914279178  (bound)
      🔒   E(4)  =   -0.1694428666  (bound)
      🔒   E(5)  =    0.5585681892  (bound)
      🔒   E(6)  =    1.8412337091  (bound)
      🔒   E(7)  =    2.2651012660  (bound)
      🔒   E(8)  =    2.2653605113  (bound)
      🌊   E(9)  =    2.7548549836  (free) 
      🌊   E(10) =    2.7548579298  (free) 
      🌊   E(11) =    2.7970433115  (free) 
      🌊   E(12) =    3.4976640375  (free) 
      🌊   E(13) =    3.4976741598  (free) 
      🌊   E(14) =    3.9044940884  (free) 

****************************************
```

![Sinusoidal Well Example](outputs/sinusoidal_well.png)

# SI Units

By default, `FDSolver` solves the Schrödinger equation in dimensionless units. However, it is also possible to perform the calculations in **SI units**. To use SI units:

1. Express the potential energy in Joules and the spatial grid in meters.
2. Set the `h_bar` and `m` attributes of the solver to their SI values (e.g. using `scipy.constants`).

Below follows an example for an electron in a finite square well:

```python
import numpy as np
from scipy import constants
from qmsolver.tise import FDSolver
from qmsolver.potentials import FiniteSquareWellPotential

well_depth_ev = 1.0     # Well depth in electron volts
well_width_nm = 1.0     # Well width in nanometers

# Convert to SI units
well_depth_joules = well_depth_ev * constants.e     # Convert eV to Joules
well_width_meters = well_width_nm * 1e-9            # Convert nm to meters

# Spatial domain in meters
x_min_m = -3e-9
x_max_m = 3e-9

solver = FDSolver(steps=2_000, x_min=x_min_m, x_max=x_max_m, n_lowest=3)

# Set physical constants in SI units
solver.h_bar = constants.hbar  # Reduced Planck's constant in J⋅s
solver.m = constants.m_e       # Electron mass in kg

potential = FiniteSquareWellPotential(
    x_grid=solver.x_grid,
    well_depth=well_depth_joules,
    well_width=well_width_meters,
)
solver.potential_generator = potential

solver.solve()
solver.output()
solver.plot(is_dimensionless=False, scale=1e19, energy_units="J")
```

```bash
****************************************

-> 3 lowest energy states:

      🔒   E(0)  = -1.29761325178584494211e-19  (bound)
      🔒   E(1)  = -4.79509995005876440109e-20  (bound)
      🌊   E(2)  = 7.54877077796044010905e-21  (free) 

****************************************
```

![SI Units Example](outputs/finite_square_well_SI_units.png)

# Convert to eV

After solving in SI units, simply divide the eigenenergies by the electron charge to get values in eV:

```python
E_lowest_ev = np.array(solver.E_lowest) / constants.e
print("\nEnergies in electron volts:")
for i, energy in enumerate(E_lowest_ev):
    print(f"E({i}) = {energy:.8f} eV")
```
```bash
Energies in electron volts:
E(0) = -0.80990649 eV
E(1) = -0.29928660 eV
E(2) = 0.04711572 eV
```

# Results Validation

## Infinite Square Well Limit

To validate the accuracy of `FDSolver` we can test it against a known analytical solution. A good test case is the **infinite square well** limit of a finite square well.

When a finite square well has a **very large depth** it tends to the infinite square well with analytical solutions:

$$E_n = n^2 \frac{\hbar^2 \pi^2}{2mL^2}$$

where:
- $n = 1, 2, 3, \dots$ (quantum number)
- $L$ is the well width
- $\hbar$ is the reduced Planck constant
- $m$ is the particle mass

Thus, we can solve a finite square well with **very large depth** (1e12 eV) using `FDSolver` and compare the results to the infinite square well formula. The finite well with very large depth eigenenergies should approach the infinite well eigenenergies.

```python
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
```

```bash
****************************************

-> 5 lowest energy states:

      🔒   E(0)  =   -0.0000001602  (bound)
      🔒   E(1)  =   -0.0000001602  (bound)
      🔒   E(2)  =   -0.0000001602  (bound)
      🔒   E(3)  =   -0.0000001602  (bound)
      🔒   E(4)  =   -0.0000001602  (bound)

****************************************

Energies in electron volts:
E(0) = 0.37585449 eV | E_ISW(0): 0.37603016 eV | Error: 0.04671698 %
E(1) = 1.50329590 eV | E_ISW(1): 1.50412065 eV | Error: 0.05483270 %
E(2) = 3.38232422 eV | E_ISW(2): 3.38427146 eV | Error: 0.05753794 %
E(3) = 6.01281738 eV | E_ISW(3): 6.01648259 eV | Error: 0.06091950 %
E(4) = 9.39514160 eV | E_ISW(4): 9.40075405 eV | Error: 0.05970214 %
```

Based on the comparison of the `FDSolver` results with the equivalent analytical solutions, we can conclude that the developed numerical method provides reliable results for bound state problems when using appropriate grid resolution. In the examined case above, the numerical results match the expected analytical values with an **error less than 0.1%**. It's worth noting that:

- In principle, accuracy improves with higher grid resolution
- However, accuracy depends on the specific grid spacing rather than just the total number of points. For instance, a grid with 6,000 steps might yield lower accuracy than one with 4,000 steps and a grid with 7,000 steps better from both. This behavior is problem-dependent and can vary between different potential functions.

The table below shows the average error for the first five eigenenergies across different grid resolutions for the validation test case above:

| Steps | Error (%) |
|-------|-----------|
| 1,000 | 0.62310486 |
| 2,000 | 1.08952827 |
| 3,000 | 0.45091440 |
| 4,000 | 0.14786237 |
| 5,000 | 0.44736513 |
| 6,000 | 0.24246108 |
| 7,000 | 0.08640829 |
| 8,000 | 0.27421701 |
| 9,000 | 0.17126452 |
| 10,000 | 0.055941852 |

# Harmonic Oscillator Validation

To further validate the accuracy of `FDSolver`, we can test it against the analytical solution for the harmonic oscillator.

The harmonic oscillator has exact analytical solutions:

$$E_n = \hbar \omega \left(n + \frac{1}{2}\right)$$

where:
- $n = 0, 1, 2, \dots$ (quantum number)
- $\omega$ is the angular frequency
- $\hbar$ is the reduced Planck constant

We can solve the harmonic oscillator potential using `FDSolver` and compare the numerical results to the analytical formula.

```python
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
    renormalized_energy = energy + np.abs(np.min(solver.potential)) / constants.e
    error = 100 * abs(renormalized_energy - analytical_energy) / analytical_energy
    s += error
    print(
        f"E({i}) = {renormalized_energy:.8f} eV | E_HO({i}): {analytical_energy:.8f} eV | Error: {error:.8f} %"
    )

print(f"\nAverage error: {s/len(E_lowest_ev):.8f} %")
```

```bash
****************************************

-> 5 lowest energy states:

      🔒   E(0)  = -4.50196327746029571420e-19  (bound)
      🔒   E(1)  = -4.39650614125021047605e-19  (bound)
      🔒   E(2)  = -4.29104905059774577557e-19  (bound)
      🔒   E(3)  = -4.18559200550213846300e-19  (bound)
      🔒   E(4)  = -4.08013500595898489953e-19  (bound)

****************************************

Energies in electron volts:
E(0) = 0.03291056 eV | E_HO(0): 0.03291060 eV | Error: 0.00010800 %
E(1) = 0.09873173 eV | E_HO(1): 0.09873179 eV | Error: 0.00006480 %
E(2) = 0.16455287 eV | E_HO(2): 0.16455299 eV | Error: 0.00007344 %
E(3) = 0.23037398 eV | E_HO(3): 0.23037418 eV | Error: 0.00008948 %
E(4) = 0.29619506 eV | E_HO(4): 0.29619538 eV | Error: 0.00010800 %
```

Based on the comparison of the `FDSolver` results with the analytical harmonic oscillator solutions, the numerical method demonstrates excellent accuracy for this potential as the numerical results match the expected analytical values with an **error less than 0.0001%** (6th decimal digit accuracy).

The accuracy in this case is much higher than the infinite square well limit validation that took place in the previous section, because the harmonic oscillator potential definition does not approximate an ideal physical system (unlike the very deep finite square well, which was a limit approximation). In the lowest energy range of the harmonic oscillator, where boundary effects are almost non-existent, the numerical description is exceptionally accurate.

The table below shows the average error for the first five eigenenergies across different grid resolutions for the harmonic oscillator test case above:

| Steps | Error (%) |
|-------|-----------|
| 1,000 | 0.00889065 |
| 2,000 | 0.00222036 |
| 3,000 | 0.00098649 |
| 4,000 | 0.00055481 |
| 5,000 | 0.00035504 |
| 6,000 | 0.00024654 |
| 7,000 | 0.00018112 |
| 8,000 | 0.00013867 |
| 9,000 | 0.00010956 |
| 10,000 | 0.00008874 |


# Development and Contributing

Based on the comparison of the `FDSolver` results with the analytical harmonic oscillator solutions, the numerical method demonstrates excellent accuracy for this potential as the numerical results match the expected analytical values with an **error less than 0.001%**.



# Development and Contributing

## Build and Test

1. Build the package: `make build`
2. Install in development mode: `make install-dev`
3. Run the test suite: `make test`

## Virtual Environment Setup

1. **Python >= 3.9** should be installed
2. **Pipenv** should be installed (if not: `pip install pipenv`)
3. Create the virtual environment: `make venv`
4. Run the test suite: `make test`

> **⚠️ Important:** For development, it is recommended to build and test from within the virtual environment.

## Additional Development Commands

- **Format code**: `make reformat` (runs black and isort)
- **Run tests with coverage**: `make coverage`
- **Create the virtual environment**: `make venv`

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

**Important Notes:**
- This is a personal project developed in my free time
- No warranty is provided
- For serious scientific work, please verify results independently and consult domain experts

## References

1. Computational Quantum Mechanics  
   Joshua Izaac, Jingbo Wang  
   Springer, Chapter 9.6: The Direct Matrix Method

2. Solving the time-dependent Schrödinger equation using finite difference methods  
   R. Becerril, F.S. Guzmán, A. Rendón-Romero, S. Valdez-Alvarado  
   *Revista Mexicana de Física E*, Vol. 54, No. 2, pp. 120-132, 2008

3. [A Python Program for Solving Schrödinger's Equation in Undergraduate Physical Chemistry](https://pubs.acs.org/doi/10.1021/acs.jchemed.7b00003)  
   Matthew N. Srnec, Shiv Upadhyay, Jeffry D. Madura  
   *Journal of Chemical Education*, Vol 94/Issue 6, 2017