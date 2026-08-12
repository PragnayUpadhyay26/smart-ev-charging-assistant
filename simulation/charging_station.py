import math


class ChargingStation:
    def __init__(
        self,
        station_id,
        name,
        latitude,
        longitude,
        total_chargers,
        charging_speed,
    ):
        # Station Information
        self.station_id = station_id
        self.name = name
        self.latitude = latitude
        self.longitude = longitude

        # Static Properties
        self.total_chargers = total_chargers
        self.charging_speed = charging_speed  # kW (e.g., 50 kW, 150 kW)

        # Dynamic Properties
        self.occupied_chargers = 0
        self.current_vehicles = []
        self.queue = []
        self.average_wait_time = 0

    def available_chargers(self):
        """Returns number of free chargers."""
        return self.total_chargers - self.occupied_chargers

    def queue_length(self):
        """Returns number of vehicles waiting in line."""
        return len(self.queue)

    def add_vehicle(self, vehicle):
        """
        Add a vehicle to the station.
        If a charger is free, start charging immediately.
        Otherwise, add the vehicle to the waiting queue.
        """
        if self.available_chargers() > 0:
            self.current_vehicles.append(vehicle)
            self.occupied_chargers += 1
        else:
            self.queue.append(vehicle)

    def remove_vehicle(self):
        """
        Remove a finished vehicle.
        If vehicles are waiting in queue, move the first one into charging.
        """
        if self.current_vehicles:
            self.current_vehicles.pop(0)
            self.occupied_chargers -= 1

        if self.queue and self.available_chargers() > 0:
            next_vehicle = self.queue.pop(0)
            self.current_vehicles.append(next_vehicle)
            self.occupied_chargers += 1

    def calculate_wait_time(self, average_session_mins=30):
        """
        Proper wait time calculation.
        - If free chargers exist: wait time is 0 mins.
        - If full: calculates waiting turns based on total chargers and queue length.
        """
        if self.available_chargers() > 0:
            self.average_wait_time = 0
            return 0

        # Calculate position for the NEXT arriving vehicle
        next_in_queue_position = self.queue_length() + 1

        # How many full charger turnover cycles needed before a charger opens
        turnover_cycles = math.ceil(next_in_queue_position / self.total_chargers)

        # Assuming vehicles are mid-session on average (half average session time remaining for current batch)
        estimated_wait = int((turnover_cycles - 0.5) * average_session_mins)

        self.average_wait_time = max(5, estimated_wait)
        return self.average_wait_time

    def get_station_status(self):
        """Returns current dynamic state of the station."""
        return {
            "station_id": self.station_id,
            "name": self.name,
            "total_chargers": self.total_chargers,
            "available_chargers": self.available_chargers(),
            "occupied_chargers": self.occupied_chargers,
            "queue_length": self.queue_length(),
            "average_wait_time": self.calculate_wait_time(),
        }