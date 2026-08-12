import os
import joblib
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split


def train():
    # Resolve paths relative to train.py location
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.abspath(
        os.path.join(BASE_DIR, "../../datasets/charging_data.csv")
    )

    if not os.path.exists(data_path):
        print(f"Error: Dataset not found at {data_path}")
        return

    df = pd.read_csv(data_path)

    # Features & Target
    X = df[[
        "battery_percentage",
        "distance",
        "total_chargers",
        "occupied_chargers",
        "queue_length",
        "charging_speed",
    ]]
    y = df["wait_time"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    mae = mean_absolute_error(y_test, predictions)
    r2 = r2_score(y_test, predictions)

    print("Model Training Complete")
    print(f"Mean Absolute Error: {mae:.2f} minutes")
    print(f"R² Score: {r2:.4f}")

    model_path = os.path.join(BASE_DIR, "wait_time_model.joblib")
    joblib.dump(model, model_path)
    print(f"Model saved directly to {model_path}")


if __name__ == "__main__":
    train()