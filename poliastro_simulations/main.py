import time
import os
from environment import simulate_orbit
from visualizer import create_czml

thrust_file = "data/thrust.csv"
last_mtime = 0

while True:
    try:
        # Check if the file has been modified
        mtime = os.path.getmtime(thrust_file)
        if mtime != last_mtime:
            last_mtime = mtime
            print("Detected change in thrust.csv, updating visualization...")
            
            # Run your simulation and create CZML
            positions = simulate_orbit()
            create_czml(positions)
            
        time.sleep(1)  # check once per second
    except KeyboardInterrupt:
        break
