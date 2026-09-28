"""
Trains two small Scikit-learn models from historical order data and saves
them to disk with joblib. Run this from the terminal whenever you have new
sales data:

    python ai_engine/train_model.py

In a real deployment this would pull rows from the Order/OrderItem tables;
here it works from a CSV export (ai_engine/sample_sales_data.csv) so it can
run standalone without a populated database.
"""
import pandas as pd
import joblib
from pathlib import Path
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "sample_sales_data.csv"


def load_data():
    return pd.read_csv(DATA_FILE)


def train_demand_model(df):
    # Features: season (numeric 1-4), past_avg_demand_kg -> Target: demand_kg
    X = df[["season", "past_avg_demand_kg"]]
    y = df["demand_kg"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = LinearRegression()
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    mae = mean_absolute_error(y_test, predictions)
    print(f"[Demand Model] Mean Absolute Error: {mae:.2f} kg")
    return model


def train_price_model(df):
    # Features: demand_kg, past_avg_price -> Target: price_per_kg
    X = df[["demand_kg", "past_avg_price"]]
    y = df["price_per_kg"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = LinearRegression()
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    mae = mean_absolute_error(y_test, predictions)
    print(f"[Price Model] Mean Absolute Error: Rs.{mae:.2f}/kg")
    return model


if __name__ == "__main__":
    df = load_data()
    demand_model = train_demand_model(df)
    price_model = train_price_model(df)

    joblib.dump(demand_model, BASE_DIR / "demand_model.pkl")
    joblib.dump(price_model, BASE_DIR / "price_model.pkl")
    print("Models saved: demand_model.pkl, price_model.pkl")
