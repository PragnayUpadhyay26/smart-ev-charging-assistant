import random


class Vehicle:
    def __init__(
        self,
        vehicle_id,
        latitude,
        longitude,
        destination_latitude,
        destination_longitude,
        battery_percentage,
    ):
        self.vehicle_id = vehicle_id

        # Current Location
        self.latitude = latitude
        self.longitude = longitude

        # Destination
        self.destination_latitude = destination_latitude
        self.destination_longitude = destination_longitude

        # Battery
        self.battery_percentage = battery_percentage

        # Simulation
        self.charging_intent = self.calculate_charging_intent()

        self.assigned_station = None

        self.wait_time = 0

    def calculate_charging_intent(self):    

        battery = self.battery_percentage

        if battery >= 90:
             probability = 0.01

        elif battery >= 80:
            probability = 0.05

        elif battery >= 70:
            probability = 0.10

        elif battery >= 60:
            probability = 0.20

        elif battery >= 50:
            probability = 0.35

        elif battery >= 40:
            probability = 0.50

        elif battery >= 30:
            probability = 0.65

        elif battery >= 20:
            probability = 0.80

        elif battery >= 10:
            probability = 0.95

        else:
            probability = 0.99

        return probability

    def needs_charging(self):
        return random.random() < self.charging_intent

    def __repr__(self):

        return (
            f"Vehicle("
            f"id={self.vehicle_id}, "
            f"battery={self.battery_percentage}%, "
            f"intent={self.charging_intent})"
        )