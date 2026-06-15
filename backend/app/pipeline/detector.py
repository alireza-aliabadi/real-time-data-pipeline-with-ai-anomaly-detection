"""Runs ML inference + rolling-window feature engineering."""
import numpy as np
from collections import deque, defaultdict
from app.ml.model import AnomalyModel
from app.config import settings


class AnomalyDetector:
    def __init__(self):
        self.model = AnomalyModel().load()
        # per-device rolling buffer for smoothing
        self._buffers: dict[str, deque] = defaultdict(
            lambda: deque(maxlen=settings.feature_window)
        )

    def _features(self, reading: dict) -> np.ndarray:
        return np.array(
            [reading["temperature"], reading["vibration"], reading["pressure"]],
            dtype=np.float64,
        )

    def detect(self, reading: dict) -> dict:
        feats = self._features(reading)
        labels, scores = self.model.predict(feats.reshape(1, -1))

        is_anomaly = labels[0] == -1
        score = float(scores[0])

        # Track per-device rolling anomaly rate
        device = reading["device_id"]
        self._buffers[device].append(1 if is_anomaly else 0)
        rolling_rate = sum(self._buffers[device]) / len(self._buffers[device])

        return {
            **reading,
            "is_anomaly": bool(is_anomaly),
            "anomaly_score": round(score, 4),
            "rolling_anomaly_rate": round(rolling_rate, 3),
            "severity": self._severity(score),
        }

    @staticmethod
    def _severity(score: float) -> str:
        if score > 0.2:
            return "high"
        if score > 0.05:
            return "medium"
        return "low"