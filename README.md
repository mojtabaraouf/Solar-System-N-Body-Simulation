# Solar System N-Body Simulation

## Overview

This Python script simulates the gravitational dynamics of the Solar System, including the Sun, Mercury, Venus, Earth, Moon, Mars, Jupiter, and Saturn, using a direct N-body approach with Newtonian gravity. The simulation runs for 10 years, capturing multiple orbits of inner planets and partial orbits of outer planets. The Earth-Moon system is emphasized, with Low Earth Orbit (LEO) and Earth-Moon Lagrange points (L1, L2) plotted as fixed dashed circles. Each body is labeled dynamically, and trajectories are visualized. The output is a GIF animation showing the orbital dynamics, suitable for astrophysical visualization and analysis.

The simulation uses the Euler integration method with a 1-day time step for simplicity, implemented with NumPy for calculations and Matplotlib/Pillow for visualization. The code is designed for educational purposes and can be extended with more sophisticated integrators (e.g., Verlet) or frameworks like AMUSE for long-term simulations.

## Features

- **Bodies**: Sun, Mercury, Venus, Earth, Moon, Mars, Jupiter, Saturn with realistic masses, semi-major axes, and orbital velocities.
- **Duration**: 10 years (~3.156e8 seconds), showing ~135 Moon orbits, 10 Earth orbits, ~41 Mercury orbits, ~16 Venus orbits, ~4 Mars orbits, ~0.84 Jupiter orbits, and ~0.34 Saturn orbits.
- **Zoom**: Plot limits of ±1.6e11 m (~1.07 AU) focus on the inner Solar System (Mercury to Mars), making the Earth-Moon orbit visible.
- **Special Orbits**:
  - **LEO**: ~400 km altitude above Earth’s surface (~6,778 km radius), plotted as a black dashed circle.
  - **L1**: ~323,136 km from Earth (~84% of Earth-Moon distance), green dashed circle.
  - **L2**: ~445,504 km from Earth (~116% of Earth-Moon distance), purple dashed circle.
- **Visualization**: Dynamic labels for each body, scaled marker sizes (Sun largest, Moon smallest), and trajectory trails. Output is a GIF (`solar_system_earth_moon_lagrange.gif`) with 20 fps.
- **Codebase**: Leverages NumPy for numerical computations, Matplotlib for plotting, and Pillow for GIF generation.

## Requirements

- Python 3.6+
- NumPy (`pip install numpy`)
- Matplotlib (`pip install matplotlib`)
- Pillow (`pip install pillow`)

## Installation

1. Clone or download the repository:
   ```bash
   git clone <repository-url>
   cd solar-system-nbody
   ```
2. Install dependencies:
   ```bash
   pip install numpy matplotlib pillow
   ```
3. Ensure the script (`solar_system_nbody_lagrange.py`) is in the working directory.

## Usage

1. Run the script:
   ```bash
   python solar_system_nbody_lagrange.py
   ```
2. The script simulates 10 years of Solar System dynamics and saves a GIF animation as `solar_system_earth_moon_lagrange.gif` in the working directory.
3. View the GIF using any image viewer or browser.

### Output
- **File**: `solar_system_earth_moon_lagrange.gif`
- **Size**: ~2-5 MB
- **Frames**: ~36 frames (10 years / 100 steps per frame)
- **FPS**: 20
- **Content**: Animated orbits of inner planets, Earth-Moon system, LEO, L1, and L2, with dynamic labels and trajectories.

## Simulation Details

- **Physics**: Uses Newton’s law of gravitation, computing pairwise forces: \( \mathbf{a}_i = \sum_{j \neq i} \frac{G m_j (\mathbf{r}_j - \mathbf{r}_i)}{|\mathbf{r}_j - \mathbf{r}_i|^3} \).
- **Integration**: Euler method with a 1-day time step (`dt = 86400 s`). Suitable for short-term simulations but may accumulate errors over longer periods.
- **Initial Conditions**: Approximate real-world values (e.g., Earth at 1 AU, Moon at ~384,400 km, orbital velocities from NASA data).
- **Limitations**:
  - 2D simulation (ignores z-axis).
  - Euler integration is less accurate for long-term dynamics.
  - Jupiter and Saturn may be out of view due to the zoomed focus (±1.6e11 m).
  - L1 and L2 are approximated; exact positions require three-body calculations.

## Customization

- **Zoom Level**: Adjust `ax.set_xlim` and `ax.set_ylim` in the script to focus closer to Earth-Moon (e.g., ±5e10 m) or include outer planets (e.g., ±1.5e12 m for Saturn).
- **Duration**: Modify `t_max` (e.g., `t_max = 30 * 365.25 * 24 * 3600` for 30 years) to see more of Saturn’s orbit, but expect increased computation time and GIF size.
- **Time Step**: Reduce `dt` (e.g., 3600 s) for higher resolution of Moon’s orbit, or increase for faster computation.
- **Labels**: Adjust label offset (`1e10` in `animate`) or fontsize for readability.
- **Advanced Integration**: Replace Euler with Velocity Verlet or use AMUSE’s `Huayno` solver for better accuracy:
  ```python
  from amuse.lab import *
  bodies = Particles(8)
  # Set masses, positions, velocities
  gravity = Huayno()
  gravity.particles.add_particles(bodies)
  gravity.evolve_model(10 | units.yr)
  ```
- **Additional Orbits**: Add L3, L4, L5 Lagrange points or other orbits by defining new `Circle` patches in the script.

## Notes for Long-Term Simulations (e.g., 4.5 Gyr)

Simulating 4.5 billion years is computationally intensive (~1.65e9 steps at 1-day dt) and requires:
- **Symplectic Integrator**: Use Verlet or AMUSE’s `Huayno`/`Hermite` for stability.
- **HPC**: Run on a cluster (e.g., Snellius) to handle computation.
- **Sparse Sampling**: Save frames every ~10,000 years for a ~100-200 frame GIF.
- **Physical Effects**: Incorporate stellar evolution (Sun’s mass loss) or tidal effects using AMUSE.

## Example Output

The GIF shows:
- Inner planets (Mercury, Venus, Earth, Moon, Mars) orbiting the Sun.
- Moon’s orbit as a small loop around Earth.
- LEO (~6,778 km radius), L1 (~323,136 km), and L2 (~445,504 km) as dashed circles around Earth.
- Dynamic labels for each body.
- Trajectories as semi-transparent lines.

## Troubleshooting

- **GIF Not Generated**: Ensure Pillow is installed (`pip install pillow`) and check for errors in the terminal.
- **Moon Not Visible**: Reduce plot limits (e.g., `ax.set_xlim(-5e10, 5e10)`) or add an inset plot for Earth-Moon.
- **Performance Issues**: Increase `dt` or reduce `t_max` for faster execution.

## Contributing

Feel free to fork the repository, suggest improvements, or add features (e.g., 3D simulation, advanced integrators). Submit pull requests or open issues on the repository.

## License

This project is licensed under the MIT License.

## Contact

For questions or suggestions, contact raouf@strw.leidenuniv.nl or open an issue on the repository.

*Last updated: June 3, 2024*
