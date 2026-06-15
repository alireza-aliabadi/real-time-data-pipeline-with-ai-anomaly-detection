import numpy as np
import pytest
from app.ml.model import AnomalyModel
from app.ml.train import generate_normal_data


@pytest.fixture(scope="module")
def trained_model():
    X = generate_normal_data(2000)
    return AnomalyModel().fit(X)


def test_model_detects_normal(trained_model):
    normal = np.array([[60.0, 0.5, 100.0]])
    labels, scores = trained_model.predict(normal)
    assert labels[0] == 1  # normal


def test_model_detects_anomaly(trained_model):
    anomaly = np.array([[105.0, 1.8, 45.0]])
    labels, scores = trained_model.predict(anomaly)
    assert labels[0] == -1  # anomaly
    assert scores[0] > 0    # higher score = more anomalous


def test_detector_output_structure(trained_model, monkeypatch, tmp_path):
    from app.pipeline import detector as det_module
    monkeypatch.setattr(det_module.AnomalyModel, "load", lambda self: trained_model)

    detector = det_module.AnomalyDetector()
    reading = {
        "device_id": "device_1",
        "timestamp": 1234567890.0,
        "temperature": 105.0,
        "vibration": 1.8,
        "pressure": 45.0,
    }
    result = detector.detect(reading)
    assert "is_anomaly" in result
    assert "anomaly_score" in result
    assert "severity" in result
    assert result["severity"] in ("low", "medium", "high")


@pytest.mark.asyncio
async def test_ws_manager_broadcast():
    from app.ws.manager import WebSocketManager

    class FakeWS:
        def __init__(self):
            self.sent = []
        async def send_text(self, msg):
            self.sent.append(msg)

    mgr = WebSocketManager()
    fake = FakeWS()
    mgr.active.append(fake)
    await mgr.broadcast({"type": "test", "data": 1})
    assert len(fake.sent) == 1