import math 
import json 
import csv 
import os

# Hohmann Transfer Conceptual Example
# Meant to guide development of algorithm on processor

G = 6.67430e-11 # gravitational constant 
M_EARTH = 5.9742e24 # kg 
mew = G*M_EARTH

def compute_burns(initial_orbit_radius, final_orbit_radius): 
    """Compute both burns required for the Hohmann Transfer to switch orbits""" 
    r_1, r_2 = initial_orbit_radius, final_orbit_radius # in meters
    a_t = (r_1 + r_2)/2 # transfer orbit major axis
    time_of_flight = math.pi*math.sqrt((a_t**3)/mew)
    delta_v_2 = (math.sqrt(mew/r_2)) - (math.sqrt(mew*( (2/r_2)-(1/a_t) ))) # v_circ_2 - v_transfer_2
    delta_v_1 = ((math.sqrt(mew*( (2/r_1)-(1/a_t) )) - math.sqrt(mew/r_1))) # v_transfer_1 - v_circ_1
    total_delta_v = delta_v_1+delta_v_2
    return delta_v_1, delta_v_2, time_of_flight



    
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
    with open(filename, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["start_time", "end_time", "delta_v"])

        # Burn 1 (at start_time)
        writer.writerow([start_time, start_time+burn_duration, delta_v1])

        # Burn 2 (after time of flight)
        writer.writerow([start_time + tof, start_time+tof+burn_duration, delta_v2])

delta_v1, delta_v2, time_of_flight = compute_burns(7000000, 12000000)
write_burns_to_csv("data/thrust.csv",5400, delta_v1, delta_v2, time_of_flight)

# Goal of processor is to perform the above calculations and also monitor burn velocity
# such that accelerometer can help calculate v_delta_measured by integrating the acceleration values
# and the processor can compare whether burn velocity has been reached for that transfer
# Have to repeat twice/two transfers per maneuver
# TLDR: MCU has to compute hohmann transfer velocities AND feedback loop for burn velocities