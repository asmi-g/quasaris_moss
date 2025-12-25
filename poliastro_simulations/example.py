import time
import csv, os, json
from model import Satellite

sat = Satellite(position=[7000000,0,0], velocity=[0,7500,0], mass=500)
dt = 10
t = 0
period_seconds = 20000
positions_file = "positions.json"

thrust_mtime = None
thrust_values = []

positions = []

while t < period_seconds:
    # Reload thrust.csv if it changed
    if os.path.exists("thrust.csv"):
        current_mtime = os.path.getmtime("thrust.csv")
        if thrust_mtime != current_mtime:
            thrust_values = []
            with open("thrust.csv") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    thrust_values.append({
                        "start_time": float(row["start_time"]),
                        "end_time": float(row["end_time"]),
                        "accel": [float(row["ax"]), float(row["ay"]), float(row["az"])]
                    })
            thrust_mtime = current_mtime

    # Determine current thrust
    thrust = None
    for event in thrust_values:
        if event["start_time"] <= t <= event["end_time"]:
            thrust = event["accel"]
            break

    # Physics step
    pos, vel, _ = sat.step(dt, thrust)
    positions.append([t, pos[0], pos[1], pos[2]])

    # Write positions.json
    with open(positions_file, "w") as f:
        json.dump(positions, f)

    t += dt
    time.sleep(dt / 10)  # slow down for "real-time" effect
