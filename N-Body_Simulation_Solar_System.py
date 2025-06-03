import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from matplotlib.patches import Circle

# Gravitational constant (m^3 kg^-1 s^-2)
G = 6.67430e-11

# Solar System bodies: masses (kg), initial positions (m), initial velocities (m/s)
bodies = [
    {'mass': 1.989e30, 'pos': np.array([0.0, 0.0]), 'vel': np.array([0.0, 0.0]), 'name': 'Sun', 'color': 'yellow', 'size': 50},
    {'mass': 3.285e23, 'pos': np.array([5.791e10, 0.0]), 'vel': np.array([0.0, 4.787e4]), 'name': 'Mercury', 'color': 'gray', 'size': 5},
    {'mass': 4.867e24, 'pos': np.array([1.082e11, 0.0]), 'vel': np.array([0.0, 3.502e4]), 'name': 'Venus', 'color': 'orange', 'size': 10},
    {'mass': 5.972e24, 'pos': np.array([1.496e11, 0.0]), 'vel': np.array([0.0, 2.978e4]), 'name': 'Earth', 'color': 'blue', 'size': 10},
    {'mass': 7.347e22, 'pos': np.array([1.496e11 + 3.844e8, 0.0]), 'vel': np.array([0.0, 2.978e4 + 1.022e3]), 'name': 'Moon', 'color': 'lightgray', 'size': 3},
    {'mass': 6.417e23, 'pos': np.array([2.279e11, 0.0]), 'vel': np.array([0.0, 2.413e4]), 'name': 'Mars', 'color': 'red', 'size': 7},
    {'mass': 1.898e27, 'pos': np.array([7.785e11, 0.0]), 'vel': np.array([0.0, 1.307e4]), 'name': 'Jupiter', 'color': 'brown', 'size': 30},
    {'mass': 5.683e26, 'pos': np.array([1.429e12, 0.0]), 'vel': np.array([0.0, 9.680e3]), 'name': 'Saturn', 'color': 'gold', 'size': 25}
]

# Time parameters
dt = 86400.0  # Time step (1 day)
t_max = 10 * 365.25 * 24 * 3600  # 10 years
n_steps = int(t_max / dt)

# Store trajectories
trajectories = [[] for _ in bodies]

# Earth-Moon Lagrange points and LEO (approximate distances in m)
earth_moon_dist = 3.844e8  # Earth-Moon distance
l1_dist = earth_moon_dist * 0.84  # L1: ~84% of Earth-Moon distance
l2_dist = earth_moon_dist * 1.16  # L2: ~116% of Earth-Moon distance
leo_dist = 6.378e6 + 4e5  # LEO: Earth radius + 400 km altitude

def compute_acceleration(pos1, pos2, mass2):
    """Calculate gravitational acceleration on body 1 due to body 2."""
    r = pos2 - pos1
    r_norm = np.linalg.norm(r)
    if r_norm < 1e3:  # Avoid division by zero
        return np.zeros(2)
    return G * mass2 * r / (r_norm ** 3)

def update_system():
    """Update positions and velocities using Euler method."""
    acc = [np.zeros(2) for _ in bodies]
    for i, body_i in enumerate(bodies):
        for j, body_j in enumerate(bodies):
            if i != j:
                acc[i] += compute_acceleration(body_i['pos'], body_j['pos'], body_j['mass'])
    
    for i, body in enumerate(bodies):
        body['vel'] += acc[i] * dt
        body['pos'] += body['vel'] * dt
        trajectories[i].append(body['pos'].copy())

# Set up plot
fig, ax = plt.subplots(figsize=(16, 16))  # Larger figure南海

# Zoom to focus on inner Solar System (up to Mars) and Earth-Moon system
ax.set_xlim(-1.e12, 1.e12)  # ~1.07 AU to include Mars
ax.set_ylim(-1.e12, 1.e12)
ax.set_xlabel('X (m)')
ax.set_ylabel('Y (m)')
ax.set_title('N-Body Simulation: Solar System (10 Years, Earth-Moon Focus)')
ax.grid(True)
ax.set_aspect('equal')

# Plot bodies, trajectories, and labels
plots = [ax.plot([], [], 'o', color=body['color'], ms=body['size'], label=body['name'])[0] for body in bodies]
trails = [ax.plot([], [], '-', color=body['color'], alpha=0.5)[0] for body in bodies]
labels = [ax.text(0, 0, body['name'], color=body['color'], fontsize=15) for body in bodies]

# Add Lagrange points and LEO as fixed dashed circles
earth_idx = 3  # Index of Earth
l1_circle = Circle((0, 0), l1_dist, fill=False, linestyle='--', color='green', label='L1')
l2_circle = Circle((0, 0), l2_dist, fill=False, linestyle='--', color='purple', label='L2')
leo_circle = Circle((0, 0), leo_dist, fill=False, linestyle='--', color='black', label='LEO')
ax.add_patch(l1_circle)
ax.add_patch(l2_circle)
ax.add_patch(leo_circle)

def init():
    """Initialize animation."""
    for plot in plots:
        plot.set_data([], [])
    for trail in trails:
        trail.set_data([], [])
    for label in labels:
        label.set_position((0, 0))
    l1_circle.center = (0, 0)
    l2_circle.center = (0, 0)
    leo_circle.center = (0, 0)
    return plots + trails + labels + [l1_circle, l2_circle, leo_circle]

def animate(i):
    """Update animation frame."""
    for _ in range(100):  # Update multiple steps per frame
        update_system()
    earth_pos = bodies[earth_idx]['pos']
    for j, (plot, trail, label) in enumerate(zip(plots, trails, labels)):
        pos = bodies[j]['pos']
        plot.set_data([pos[0]], [pos[1]])
        traj = np.array(trajectories[j])
        trail.set_data(traj[:, 0], traj[:, 1])
        label.set_position((pos[0] + 1e10, pos[1] + 1e10))
    # Update Lagrange points and LEO relative to Earth's position
    l1_circle.center = (earth_pos[0] + l1_dist, earth_pos[1])
    l2_circle.center = (earth_pos[0] + l2_dist, earth_pos[1])
    leo_circle.center = (earth_pos[0], earth_pos[1])
    return plots + trails + labels + [l1_circle, l2_circle, leo_circle]

# Create animation
ani = FuncAnimation(fig, animate, frames=n_steps//100, init_func=init, blit=True, interval=10)
ax.legend()

# Save as GIF
writer = PillowWriter(fps=10)
ani.save('solar_system_earth_moon_lagrange.gif', writer=writer)
print("GIF saved as 'solar_system_earth_moon_lagrange.gif'")
plt.close()
