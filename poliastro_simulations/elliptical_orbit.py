import math
import json
from datetime import datetime, timedelta

# Define constants as parameters
mass_1 = 1
mass_2 = 1
acceleration = 1
r_distance = 1

# Newton's Second Law
force = mass_1 * acceleration

# Example Defines
universal_constant = 6.67259*(math.pow(10, -11)) # Units: N-m2/kg2
mass_earth = 5.9742*(math.pow(10, 24))  # Units: kg
gravitational_acceleration_earth = 9.80665 # Units: m/s^2


# Law of Universal Gravitation
force_g = universal_constant * ((mass_1*mass_2)/r_distance*r_distance)
force_earth_g = universal_constant*mass_earth / (r_distance*r_distance)

# Orbiting Body Formulae - Circular Orbit
velocity_body = math.sqrt(universal_constant*mass_earth/r_distance)

# Equation of Elliptical Orbit
a = 7000000  # semi-major axis (X)
b = 7000000  # semi-minor axis (Y)
tilt_angle_deg = 5
tilt_angle_rad = math.radians(tilt_angle_deg)
period_seconds = 4800  # 90 minutes
step = 600  # one position every 10 minutes
positions = []

for t in range(0, period_seconds + 1, step):
    # θ from 0 to 2π
    theta = (2 * math.pi) * (t / period_seconds)

    # 2D Ellipse Parametric Equations
    x = a * math.cos(theta) 
    y = b * math.sin(theta) 
    z = 0  # orbit lies in XY plane

    # Rotate the ellipse around the X-axis (chosen arbitrarily) by the tilt angle
    y_rot = y * math.cos(tilt_angle_rad) - z * math.sin(tilt_angle_rad)
    z_rot = y * math.sin(tilt_angle_rad) + z * math.cos(tilt_angle_rad)

    positions += [t, x, y_rot, z_rot]

# result: CZML list of generated Cartesian Coordinates
print(positions)