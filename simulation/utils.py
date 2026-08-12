import math

def calculate_distance(lat1, lon1, lat2, lon2):
    """
    Returns Euclidean distance.
    Good enough for the MVP.
    """

    return math.sqrt(
        (lat1 - lat2) ** 2 +
        (lon1 - lon2) ** 2
    )
def calculate_station_score(vehicle, station, distance):

    # Normalize values
    distance_score = distance * 100

    wait_score = station.calculate_wait_time()

    availability_score = (
        station.total_chargers - station.occupied_chargers
    ) * 5

    battery_penalty = (100 - vehicle.battery_percentage) * 0.5

    score = (
        distance_score
        + wait_score
        - availability_score
        - battery_penalty
    )

    return score