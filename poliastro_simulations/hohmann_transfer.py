import math 
import json 
import csv 
import os

# Hohmann Transfer Example

G = 6.67430e-11 # gravitational constant 
M_EARTH = 5.9742e24 # kg 
mew = G*M_EARTH

def compute_burns_unused(initial_orbit_radius, final_orbit_radius): 
    """Compute both burns required for the Hohmann Transfer to switch orbits""" 
    r_1, r_2 = initial_orbit_radius, final_orbit_radius # in meters
    a_t = (r_1 + r_2)/2 # transfer orbit major axis
    time_of_flight = math.pi()*math.sqrt((a_t**3)/mew)
    if (r_1<r_2):
        #insert logic here
        delta_v_1 = abs( (math.sqrt(mew/r_2)) - (math.sqrt(mew*( (2/r_2)-(1/a_t) ))) )
        delta_v_2 = abs( (math.sqrt(mew/r_1)) - (math.sqrt(mew*( (2/r_1)-(1/a_t) ))) ) 
        total_delta_v = delta_v_1+delta_v_2
        return delta_v_1, delta_v_2, time_of_flight
    if (r_1>r_2):
        #insert logic here
        delta_v_1 = abs( (math.sqrt(mew/r_2)) - (math.sqrt(mew*( (2/r_1)-(1/a_t) ))) )
        delta_v_2 = abs( (math.sqrt(mew/r_1)) - (math.sqrt(mew*( (2/r_2)-(1/a_t) ))) )
        total_delta_v = delta_v_1+delta_v_2
        return delta_v_1, delta_v_2, time_of_flight
    
def compute_burns_second(r1, r2):
    """
    Compute Hohmann transfer burns between two circular orbits.
    Returns: delta_v1, delta_v2, time_of_flight
    """
    mu = mew

    a_t = (r1 + r2) / 2.0  # semi-major axis of transfer orbit

    # Circular orbit velocities
    v_circ_1 = math.sqrt(mu / r1)
    v_circ_2 = math.sqrt(mu / r2)

    # Transfer orbit velocities
    v_trans_1 = math.sqrt(mu * (2/r1 - 1/a_t))  # periapsis
    v_trans_2 = math.sqrt(mu * (2/r2 - 1/a_t))  # apoapsis

    delta_v1 = v_trans_1 - v_circ_1
    delta_v2 = v_circ_2 - v_trans_2

    # Time of flight (half orbit)
    time_of_flight = math.pi * math.sqrt(a_t**3 / mu)

    return delta_v1, delta_v2, time_of_flight

    
def write_burns_to_csv(
    filename,
    start_time,
    delta_v1,
    delta_v2,
    tof,
    burn_duration=60.0
):
    """
    Writes two Hohmann burns to CSV in acceleration format.
    Acceleration is applied in +X direction (placeholder).
    """

    a1 = delta_v1 / burn_duration
    a2 = delta_v2 / burn_duration

    with open(filename, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["start_time", "end_time", "delta_v"])

        # Burn 1 (at start_time)
        writer.writerow([start_time, start_time+burn_duration, delta_v1])

        # Burn 2 (after time of flight)
        writer.writerow([start_time + tof, start_time+tof+burn_duration, delta_v2])

delta_v1, delta_v2, time_of_flight = compute_burns_second(7000000, 9000000)
write_burns_to_csv("thrust.csv",5400, delta_v1, delta_v2, time_of_flight)