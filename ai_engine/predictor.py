import joblib
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DEMAND_MODEL_PATH = BASE_DIR / "demand_model.pkl"
PRICE_MODEL_PATH = BASE_DIR / "price_model.pkl"

_demand_model = None
_price_model = None


def _load_models():
    global _demand_model, _price_model
    if _demand_model is None:
        _demand_model = joblib.load(DEMAND_MODEL_PATH)
    if _price_model is None:
        _price_model = joblib.load(PRICE_MODEL_PATH)


def predict_demand_and_price(season: int, past_avg_demand_kg: float, past_avg_price: float):
    """
    Pipeline: Historical Data -> Clean Data -> Select Features -> Train Model
    -> Evaluate -> Predict  (this function is the "Predict" step; training
    happens separately in train_model.py, matching how real ML systems
    separate offline training from online inference).
    """
    _load_models()

    predicted_demand = _demand_model.predict([[season, past_avg_demand_kg]])[0]
    predicted_price = _price_model.predict([[predicted_demand, past_avg_price]])[0]

    return {
        "predicted_demand_kg": round(float(predicted_demand), 1),
        "recommended_price_low": round(float(predicted_price) * 0.95, 2),
        "recommended_price_high": round(float(predicted_price) * 1.05, 2),
    }


if __name__ == "__main__":
    # Quick manual test matching the PPT's example: Tomato -> demand -> price range
    result = predict_demand_and_price(season=2, past_avg_demand_kg=900, past_avg_price=35)
    print("Tomato prediction:")
    print(f"  Predicted demand : {result['predicted_demand_kg']} KG")
    print(f"  Recommended price: Rs.{result['recommended_price_low']}"
          f" - Rs.{result['recommended_price_high']} / KG")
