import json
import math
from datetime import datetime, timedelta

def create_czml(positions, period_seconds=100000, step_seconds=600):
    quaternions = []
    for t in range(0, period_seconds + 1, step_seconds):
        angle_rad = math.radians(t * 0.5)
        half_angle = angle_rad / 2
        x, y, z = 0.0, 0.0, math.sin(half_angle)
        w = math.cos(half_angle)
        quaternions.extend([t, x, y, z, w])

    start_time = datetime(2025, 10, 9, 0, 0, 0)
    end_time = start_time + timedelta(seconds=period_seconds)
    iso_start = start_time.strftime('%Y-%m-%dT%H:%M:%SZ')
    iso_end = end_time.strftime('%Y-%m-%dT%H:%M:%SZ')

    czml = [
        {"id": "document", "version": "1.0",
         "clock": {"interval": f"{iso_start}/{iso_end}", "currentTime": iso_start,
                   "multiplier": 60, "range": "LOOP_STOP", "step": "SYSTEM_CLOCK_MULTIPLIER"}},
        {"id": "satellite", "name": "MyOrbitingObject", "availability": f"{iso_start}/{iso_end}",
         "position": {"epoch": iso_start, "interpolationAlgorithm": "LAGRANGE",
                      "interpolationDegree": 5, "referenceFrame": "INERTIAL", "cartesian": positions},
         "orientation": {"epoch": iso_start, "unitQuaternion": quaternions},
         "point": {"color": {"rgba": [255,0,0,255]}, "pixelSize": 10},
         "label": {"text": "Satellite", "font": "14pt sans-serif", "horizontalOrigin": "LEFT",
                   "pixelOffset": {"cartesian2": [10, 0]}, "fillColor": {"rgba": [255,255,0,255]}},
         "path": {"material": {"solidColor": {"color": {"rgba": [0,255,255,255]}}}, "width": 2, "resolution": 120},
         "model": {"gltf": "model_deep_space_1.glb", "scale": 1.0, "minimumPixelSize": 100, "maximumPixelSize": 1000}}
    ]

    with open("data/orbit.czml", "w") as f:
        json.dump(czml, f, indent=2)


if __name__ == "__main__":
    # Read positions saved from environment.py
    with open("data/positions.json") as f:
        positions = json.load(f)
    create_czml(positions)
