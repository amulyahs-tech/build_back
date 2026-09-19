import os
import json
import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline


def generate_synthetic_dataset(n_samples: int = 2500, random_state: int = 42) -> pd.DataFrame:
    """Generates synthetic construction second-market price valuation dataset."""
    np.random.seed(random_state)

    materials = [
        "Bricks", "Concrete", "Cement Blocks", "Steel / Rebar", "Wood / Timber",
        "Tiles", "Glass", "PVC Pipes", "Metal Pipes", "Doors", "Windows",
        "Roofing Materials", "Stones", "Sand", "Marble", "Granite", "Ceramic Materials"
    ]

    base_rates = {
        "Bricks": 6.5, "Concrete": 1800.0, "Cement Blocks": 24.0, "Steel / Rebar": 42.0,
        "Wood / Timber": 750.0, "Tiles": 28.0, "Glass": 45.0, "PVC Pipes": 80.0,
        "Metal Pipes": 210.0, "Doors": 2600.0, "Windows": 1700.0, "Roofing Materials": 220.0,
        "Stones": 650.0, "Sand": 900.0, "Marble": 65.0, "Granite": 58.0, "Ceramic Materials": 28.0
    }

    cities = ["Bangalore", "Mumbai", "Delhi", "Hyderabad", "Pune", "Chennai", "Mysore"]
    city_weights = {"Bangalore": 1.15, "Mumbai": 1.25, "Delhi": 1.18, "Hyderabad": 1.10, "Pune": 1.08, "Chennai": 1.07, "Mysore": 0.95}

    records = []
    for _ in range(n_samples):
        mat = np.random.choice(materials)
        city = np.random.choice(cities)
        quality_score = float(np.random.uniform(25.0, 98.0))
        age_years = float(np.random.uniform(0.5, 12.0))
        damage_pct = float(np.random.uniform(2.0, 60.0))

        # realistic quantity distribution based on material
        if mat in ["Concrete", "Stones", "Sand"]:
            quantity = float(np.random.uniform(5.0, 150.0))
        elif mat in ["Bricks", "Cement Blocks", "Tiles"]:
            quantity = float(np.random.uniform(200.0, 5000.0))
        elif mat in ["Steel / Rebar"]:
            quantity = float(np.random.uniform(100.0, 3000.0))
        else:
            quantity = float(np.random.uniform(5.0, 100.0))

        base_unit = base_rates[mat]
        c_mult = city_weights[city]

        q_factor = 0.3 + 0.7 * (quality_score / 100.0)
        age_factor = max(0.4, 1.0 - (age_years * 0.04))
        dam_factor = max(0.3, 1.0 - (damage_pct / 140.0))

        # Price formula with slight realistic noise
        noise = float(np.random.normal(1.0, 0.03))
        unit_rate = base_unit * q_factor * age_factor * dam_factor * c_mult * noise
        total_price = unit_rate * quantity

        records.append({
            "material": mat,
            "city": city,
            "quality_score": quality_score,
            "age_years": age_years,
            "damage_pct": damage_pct,
            "quantity": quantity,
            "total_price": max(100.0, total_price)
        })

    return pd.DataFrame(records)


def train_and_evaluate():
    """Trains regression models and serializes Gradient Boosting Regressor."""
    print("Generating training dataset...")
    df = generate_synthetic_dataset(n_samples=3000, random_state=42)

    X = df[["material", "city", "quality_score", "age_years", "damage_pct", "quantity"]]
    y = df["total_price"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    categorical_features = ["material", "city"]
    numerical_features = ["quality_score", "age_years", "damage_pct", "quantity"]

    preprocessor = ColumnTransformer(
        transformers=[
            ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features),
            ("num", "passthrough", numerical_features)
        ]
    )

    models = {
        "Linear Regression": LinearRegression(),
        "Random Forest": RandomForestRegressor(n_estimators=100, max_depth=12, random_state=42),
        "Gradient Boosting Regressor": GradientBoostingRegressor(n_estimators=150, learning_rate=0.08, max_depth=6, random_state=42)
    }

    metrics_report = {}
    best_pipeline = None

    for name, model in models.items():
        pipeline = Pipeline(steps=[("preprocessor", preprocessor), ("regressor", model)])
        pipeline.fit(X_train, y_train)

        preds = pipeline.predict(X_test)
        mae = float(mean_absolute_error(y_test, preds))
        rmse = float(np.sqrt(mean_squared_error(y_test, preds)))
        r2 = float(r2_score(y_test, preds))

        print(f"[{name}] MAE: INR {mae:,.2f} | RMSE: INR {rmse:,.2f} | R2: {r2:.4f}")

        metrics_report[name] = {
            "mae": round(mae, 2),
            "rmse": round(rmse, 2),
            "r2": round(r2, 4)
        }

        if name == "Gradient Boosting Regressor":
            best_pipeline = pipeline

    # Ensure output directory exists
    out_dir = os.path.join(os.path.dirname(__file__), "..", "models")
    os.makedirs(out_dir, exist_ok=True)

    # Save model
    model_path = os.path.join(out_dir, "gradient_boosting_price_model.joblib")
    joblib.dump(best_pipeline, model_path)
    print(f"Successfully saved Gradient Boosting model to: {model_path}")

    # Save metrics JSON
    metrics_path = os.path.join(out_dir, "model_metrics.json")
    with open(metrics_path, "w") as f:
        json.dump(metrics_report, f, indent=2)
    print(f"Successfully saved evaluation metrics to: {metrics_path}")


if __name__ == "__main__":
    train_and_evaluate()
