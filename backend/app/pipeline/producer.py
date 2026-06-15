"""Simulates IoT sensors pushing data into a Redis Stream."""
import asyncio
import json
import time
import random
import redis.asyncio as redis
from app.config import settings


class DataProducer:
    def __init__(self):
        self.redis = redis.Redis(
            host=settings.redis_host, port=settings.redis_port, decode_responses=True
        )
        self._running = False

    def _generate_reading(self) -> dict:
        # ~5% chance to inject an anomaly
        anomaly = random.random() < 0.05
        if anomaly:
            temperature = random.uniform(85, 110)   # overheating
            vibration = random.uniform(1.2, 2.0)    # excessive vibration
            pressure = random.uniform(40, 60)       # pressure drop
        else:
            temperature = random.gauss(60, 5)
            vibration = random.gauss(0.5, 0.1)
            pressure = random.gauss(100, 8)

        return {
            "device_id": f"device_{random.randint(1, 5)}",
            "timestamp": time.time(),
            "temperature": round(temperature, 2),
            "vibration": round(max(vibration, 0), 3),
            "pressure": round(pressure, 2),
            "_injected_anomaly": int(anomaly),  # ground truth for demo
        }

    async def start(self):
        self._running = True
        interval = settings.produce_interval_ms / 1000
        print("[Producer] Started.")
        while self._running:
            reading = self._generate_reading()
            await self.redis.xadd(
                settings.redis_stream,
                {"data": json.dumps(reading)},
                maxlen=10000,  # cap stream memory
                approximate=True,
            )
            await asyncio.sleep(interval)

    async def stop(self):
        self._running = False
        await self.redis.aclose()