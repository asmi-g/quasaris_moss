from environment import simulate_orbit
from visualizer import create_czml


positions = simulate_orbit()
create_czml(positions)
