"""Train an initial anomaly model on synthetic 'normal' data.

Run once: python -m app.ml.train
"""
import numpy as np
from app.ml.model import AnomalyModel


def generate_normal_data(n: int = 5000) -> np.ndarray:
    """Simulate normal sensor readings: temperature, vibration, pressure."""
    rng = np.random.default_rng(42)
    temperature = rng.normal(loc=60, scale=5, size=n)
    vibration = rng.normal(loc=0.5, scale=0.1, size=n)
    pressure = rng.normal(loc=100, scale=8, size=n)
    return np.column_stack([temperature, vibration, pressure])


def main():
    print("Generating training data...")
    X = generate_normal_data()
    print(f"Training IsolationForest on {X.shape[0]} samples...")
    model = AnomalyModel().fit(X)
    model.save()
    print("Model saved successfully.")


if __name__ == "__main__":
    main()