import math 
import json 
import csv 
import os
from datetime import datetime, timedelta 
from model import Satellite

# TO-DO: Look into Hohmann Transfer for determining thrust values and timings on MCU

def read_thrust_values(filename="thrust.csv"):
    """
    Read a list of thrust readings from a CSV.
    Each entry in thrust.csv will be written as:
    {'start_time','end_time', 'delta_v'}
    """
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

def write_accelerometer_values(imu_accel_values, filename="acceleration.csv"):
    """
    Write a list of accelerometer readings to CSV.
    Each entry in accel_data should be a dict:
    {'time': t, 'ax': ax, 'ay': ay, 'az': az}
    """
    file_exists = os.path.exists(filename)
    with open(filename, "w", newline="") as csvfile:  # append mode
        writer = csv.writer(csvfile)
        writer.writerow(["time", "ax", "ay", "az"])  # header
        for t, ax, ay, az in imu_accel_values:
            writer.writerow([t, ax, ay, az])

G = 6.67430e-11 # gravitational constant 
M_EARTH = 5.9742e24 # kg 
mew = G*M_EARTH

sat = Satellite( 
        position=[7000000, 0, 0], # starting at periapsis 
        velocity=[0, math.sqrt(mew/7000000), 0], # roughly circular orbit 
        mass=500 
) 

t = 0 
dt = 10 # seconds 
burn_duration=60
positions = [] 
imu_accel_values = []
period_seconds = 50000 
max_steps = 10000 # or while True for truly infinite 
    
thrust_values = read_thrust_values("thrust.csv") # pick latest thrust (or last one if we ran out) 

for step_idx in range(max_steps): 
    thrust = None
    for event in thrust_values:
        if event["start_time"] <= t <= event["end_time"]:
            burn_duration = event["end_time"] - event["start_time"]
            dv = event["delta_v"]

            # Current velocity vector
            vx, vy, vz = sat.velocity
            v_mag = math.sqrt(vx*vx + vy*vy + vz*vz)

            if v_mag > 0:
                v_hat = [vx/v_mag, vy/v_mag, vz/v_mag]

                # Acceleration magnitude
                a_mag = dv / burn_duration

                thrust = [
                    a_mag * v_hat[0],
                    a_mag * v_hat[1],
                    a_mag * v_hat[2]
                ]
            break      
    pos, vel, accel = sat.step(dt, thrust) 
    positions.extend([t, pos[0], pos[1], pos[2]]) 

    # Record the acceleration
    imu_accel_values.append([t, accel[0], accel[1], accel[2]])

    t += dt # simple accelerometer in body frame (here same as inertial for simplicity)     
    
write_accelerometer_values(imu_accel_values,"acceleration.csv")

step = 600 # one position every 10 minutes 
quaternions = [] 
for t in range(0, period_seconds + 1, step): # Simulate a rotation of 1 degree per time step around Z axis 
    angle_rad = math.radians(t * 0.5) # 0.5 deg/sec = 30 deg per minute 
    half_angle = angle_rad / 2 
    x = 0.0 
    y = 0.0 
    z = math.sin(half_angle) 
    w = math.cos(half_angle) 
    quaternions.extend([t, x, y, z, w]) 
    
# Define CZML content 
start_time = datetime(2025, 10, 9, 0, 0, 0) 
end_time = start_time + timedelta(seconds=period_seconds) 
iso_start = start_time.strftime('%Y-%m-%dT%H:%M:%SZ') 
iso_end = end_time.strftime('%Y-%m-%dT%H:%M:%SZ') 
czml = [ 
    { 
        "id": "document", 
        "version": "1.0", 
        "clock": { 
            "interval": f"{iso_start}/{iso_end}", 
            "currentTime": iso_start, 
            "multiplier": 60, 
            "range": "LOOP_STOP", 
            "step": "SYSTEM_CLOCK_MULTIPLIER" 
        } 
    }, 
    { 
        "id": "satellite", 
        "name": "MyOrbitingObject", 
        "availability": f"{iso_start}/{iso_end}", 
        "position": { 
            "epoch": iso_start, 
            "interpolationAlgorithm": "LAGRANGE", 
            "interpolationDegree": 5, 
            "referenceFrame": "INERTIAL", 
            "cartesian": positions 
        }, 
        "orientation": { 
                "epoch": iso_start, 
                "unitQuaternion": quaternions 
        }, 
        "point": { 
                "color": {
                    "rgba": [255, 0, 0, 255]
                }, 
                "pixelSize": 10 
        }, 
        "label": { 
                "text": "Satellite", 
                "font": "14pt sans-serif", 
                "horizontalOrigin": "LEFT", 
                "pixelOffset": {"cartesian2": [10, 0]}, 
                "fillColor": {"rgba": [255, 255, 0, 255]} 
        }, 
        "path": { 
                "material": { 
                    "solidColor": { 
                        "color": {
                        "rgba": [0, 255, 255, 255]} 
                    } 
                }, 
                "width": 2, 
                "resolution": 120 
        }, 
        "model": { 
                "gltf": "model_deep_space_1.glb", "scale": 1.0, "minimumPixelSize": 100, "maximumPixelSize": 1000, 
        } 
    } 
] 

czml[1]["position"]["cartesian"] = positions 
with open("orbit.czml", "w") as f: 
    json.dump(czml, f, indent=2)