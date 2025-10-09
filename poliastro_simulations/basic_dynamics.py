import math

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