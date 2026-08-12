import random

from vehicle import Vehicle
from utils import calculate_distance, calculate_station_score
from stations import stations


def recommend_station(vehicle):
    best_station = None
    best_score = float("inf")

    for station in stations:
        distance = calculate_distance(
            vehicle.latitude,
            vehicle.longitude,
            station.latitude,
            station.longitude,
        )

        score = calculate_station_score(
            vehicle,
            station,
            distance,
        )

        if score < best_score:
            best_score = score
            best_station = station

    return best_station


# 1. Generate Vehicles
vehicles = []
for i in range(100):
    vehicle = Vehicle(
        vehicle_id=i + 1,
        latitude=random.uniform(18.45, 18.65),
        longitude=random.uniform(73.72, 73.95),
        destination_latitude=random.uniform(18.45, 18.65),
        destination_longitude=random.uniform(73.72, 73.95),
        battery_percentage=random.randint(5, 100),
    )
    vehicles.append(vehicle)

# 2. Process Vehicles and Assign Stations
charging_count = 0
for vehicle in vehicles:
    if vehicle.needs_charging():
        charging_count += 1
        station = recommend_station(vehicle)
        if station:
            station.add_vehicle(vehicle)
            vehicle.assigned_station = station.name

# 3. Print Results
print(f"\nTotal vehicles needing charging: {charging_count}")

print("\n--- Vehicle Recommendations (First 15 Vehicles) ---")
for vehicle in vehicles[:15]:
    if vehicle.assigned_station:
        print(
            f"Vehicle {vehicle.vehicle_id} "
            f"(Battery {vehicle.battery_percentage}%) "
            f"→ Assigned to: {vehicle.assigned_station}"
        )
    else:
        print(
            f"Vehicle {vehicle.vehicle_id} "
            f"(Battery {vehicle.battery_percentage}%) "
            f"→ Does not need charging"
        )

print("\n--- Station Status ---")
for station in stations:
    print(f"\nStation: {station.name}")
    print(f"Occupied: {station.occupied_chargers}/{station.total_chargers}")
    print(f"Queue: {station.queue_length()}")
    print(f"Wait: {station.calculate_wait_time()} minutes")