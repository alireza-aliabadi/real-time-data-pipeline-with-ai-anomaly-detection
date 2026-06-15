import os
import joblib
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from app.config import settings


class AnomalyModel:
    """Lightweight IsolationForest-based anomaly detector.

    IsolationForest is fast and memory-efficient — ideal for low-spec hardware.
    """

    def __init__(self):
        self.model: IsolationForest | None = None
        self.scaler: StandardScaler | None = None

    def fit(self, X: np.ndarray):
        self.scaler = StandardScaler()
        X_scaled = self.scaler.fit_transform(X)

        self.model = IsolationForest(
            n_estimators=100,
            contamination=settings.contamination,
            max_samples=256,      # keeps memory low
            n_jobs=2,             # use 2 of your 4 cores
            random_state=42,
        )
        self.model.fit(X_scaled)
        return self

    def predict(self, X: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        """Returns (labels, scores). label: -1 anomaly, 1 normal."""
        X_scaled = self.scaler.transform(X)
        labels = self.model.predict(X_scaled)
        # decision_function: higher = more normal. Negate so higher = more anomalous
        scores = -self.model.decision_function(X_scaled)
        return labels, scores

    def save(self):
        os.makedirs(os.path.dirname(settings.model_path), exist_ok=True)
        joblib.dump(self.model, settings.model_path)
        joblib.dump(self.scaler, settings.scaler_path)

    def load(self):
        self.model = joblib.load(settings.model_path)
        self.scaler = joblib.load(settings.scaler_path)
        return self

    def is_loaded(self) -> bool:
        return self.model is not None and self.scaler is not None