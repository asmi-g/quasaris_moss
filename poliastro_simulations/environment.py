import math
import csv
import json
from model import Satellite

G = 6.67430e-11
M_EARTH = 5.9742e24
mew = G * M_EARTH

def read_thrust_values(filename="data/thrust.csv"):
    events = []
    with open(filename, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            events.append({
                "start_time": float(row["start_time"]),
                "end_time": float(row["end_time"]),
                "delta_v": float(row["delta_v"])
            })
    return events

def write_accelerometer_values(imu_accel_values, filename="data/acceleration.csv"):
    with open(filename, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["time", "ax", "ay", "az"])
        for t, ax, ay, az in imu_accel_values:
            writer.writerow([t, ax, ay, az])

def simulate_orbit():
    sat = Satellite(
        position=[7000000, 0, 0],
        velocity=[0, math.sqrt(mew/7000000), 0],
        mass=500
    )

    dt = 10
    positions = []
    imu_accel_values = []
    t = 0
    max_steps = 10000

    thrust_values = read_thrust_values("data/thrust.csv")

    for step_idx in range(max_steps):
        thrust = None
        for event in thrust_values:
            if event["start_time"] <= t <= event["end_time"]:
                burn_duration = event["end_time"] - event["start_time"]
                dv = event["delta_v"]

                vx, vy, vz = sat.velocity
                v_mag = math.sqrt(vx*vx + vy*vy + vz*vz)
                if v_mag > 0:
                    v_hat = [vx/v_mag, vy/v_mag, vz/v_mag]
                    a_mag = dv / burn_duration
                    thrust = [a_mag * v_hat[i] for i in range(3)]
                break

        pos, vel, accel = sat.step(dt, thrust)
        positions.extend([t, pos[0], pos[1], pos[2]])
        imu_accel_values.append([t, accel[0], accel[1], accel[2]])
        t += dt

    write_accelerometer_values(imu_accel_values, "data/acceleration.csv")

    # Save positions for visualization
    with open("data/positions.json", "w") as f:
        json.dump(positions, f)

    return positions
