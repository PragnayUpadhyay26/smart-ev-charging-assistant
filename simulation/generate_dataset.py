import csv
import os
import random

from stations import stations
from utils import calculate_distance, calculate_station_score
from vehicle import Vehicle


def generate_data():
    # Resolve absolute path to datasets folder relative to this file
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    dataset_dir = os.path.abspath(os.path.join(BASE_DIR, "../datasets"))
    os.makedirs(dataset_dir, exist_ok=True)
    dataset_path = os.path.join(dataset_dir, "charging_data.csv")

    headers = [
        "battery_percentage",
        "distance",
        "total_chargers",
        "occupied_chargers",
        "queue_length",
        "charging_speed",
        "wait_time",
    ]

    rows = []

    # Run 50 simulation cycles across fluctuating dynamic loads
    for _ in range(50):
        # Reset station state per cycle
        for station in stations:
            station.occupied_chargers = 0
            station.queue = []
            station.current_vehicles = []

        # Generate 100 arriving vehicles per cycle
        for i in range(100):
            vehicle = Vehicle(
                vehicle_id=i + 1,
                latitude=random.uniform(18.45, 18.65),
                longitude=random.uniform(73.72, 73.95),
                destination_latitude=random.uniform(18.45, 18.65),
                destination_longitude=random.uniform(73.72, 73.95),
                battery_percentage=random.randint(5, 100),
            )

            # Record features and dynamic target whenever a vehicle seeks charging
            if vehicle.needs_charging():
                for station in stations:
                    dist = calculate_distance(
                        vehicle.latitude,
                        vehicle.longitude,
                        station.latitude,
                        station.longitude,
                    )
                    wait_time = station.calculate_wait_time()

                    rows.append([
                        vehicle.battery_percentage,
                        round(dist, 4),
                        station.total_chargers,
                        station.occupied_chargers,
                        station.queue_length(),
                        station.charging_speed,
                        wait_time,
                    ])

                # Dynamic station selection and assignment
                best_station = None
                best_score = float("inf")
                for station in stations:
                    dist = calculate_distance(
                        vehicle.latitude,
                        vehicle.longitude,
                        station.latitude,
                        station.longitude,
                    )
                    score = calculate_station_score(vehicle, station, dist)
                    if score < best_score:
                        best_score = score
                        best_station = station

                if best_station:
                    best_station.add_vehicle(vehicle)

    with open(dataset_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)

    print(f"Successfully generated {len(rows)} samples into {dataset_path}")


if __name__ == "__main__":
    generate_data()