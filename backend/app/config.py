from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_stream: str = "sensor_stream"
    redis_group: str = "anomaly_group"
    redis_consumer: str = "consumer_1"

    model_path: str = "models/anomaly_model.joblib"
    scaler_path: str = "models/scaler.joblib"

    # Anomaly detection
    contamination: float = 0.02  # expected fraction of anomalies
    feature_window: int = 10     # rolling window size

    # Producer
    produce_interval_ms: int = 200  # 5 msgs/sec

    class Config:
        env_file = ".env"


settings = Settings()