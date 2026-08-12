CREATE TABLE charging_stations (
    station_id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    latitude DECIMAL(9,6),
    longitude DECIMAL(9,6),
    charger_count INT,
    charging_speed INT,
    operator VARCHAR(50)
);

CREATE TABLE vehicles (
    vehicle_id SERIAL PRIMARY KEY,
    battery_percent FLOAT,
    latitude DECIMAL(9,6),
    longitude DECIMAL(9,6),
    destination_latitude DECIMAL(9,6),
    destination_longitude DECIMAL(9,6),
    charging_intent FLOAT
);

CREATE TABLE queue_status (
    station_id INT PRIMARY KEY,
    occupied_chargers INT,
    queue_length INT,
    average_wait_time FLOAT,
    last_updated TIMESTAMP
);

CREATE TABLE predictions (
    prediction_id SERIAL PRIMARY KEY,
    station_id INT,
    predicted_wait_time FLOAT,
    timestamp TIMESTAMP
);