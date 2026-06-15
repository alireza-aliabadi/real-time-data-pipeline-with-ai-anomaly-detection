"""Consumes from Redis Stream, runs detection, broadcasts via WebSocket."""
import asyncio
import json
import redis.asyncio as redis
from redis.exceptions import ResponseError
from app.config import settings
from app.pipeline.detector import AnomalyDetector
from app.ws.manager import ws_manager


class StreamConsumer:
    def __init__(self):
        self.redis = redis.Redis(
            host=settings.redis_host, port=settings.redis_port, decode_responses=True
        )
        self.detector = AnomalyDetector()
        self._running = False
        self.stats = {"processed": 0, "anomalies": 0}

    async def _ensure_group(self):
        try:
            await self.redis.xgroup_create(
                settings.redis_stream, settings.redis_group, id="0", mkstream=True
            )
        except ResponseError as e:
            if "BUSYGROUP" not in str(e):
                raise

    async def start(self):
        await self._ensure_group()
        self._running = True
        print("[Consumer] Started.")
        while self._running:
            try:
                resp = await self.redis.xreadgroup(
                    settings.redis_group,
                    settings.redis_consumer,
                    {settings.redis_stream: ">"},
                    count=20,
                    block=1000,
                )
            except Exception as e:
                print(f"[Consumer] read error: {e}")
                await asyncio.sleep(1)
                continue

            if not resp:
                continue

            for _stream, messages in resp:
                for msg_id, fields in messages:
                    await self._process(msg_id, fields)
    async def _process(self, msg_id: str, fields: dict):
        try:
            reading = json.loads(fields["data"])
            result = self.detector.detect(reading)

            self.stats["processed"] += 1
            if result["is_anomaly"]:
                self.stats["anomalies"] += 1

            # Broadcast to all connected WebSocket clients
            await ws_manager.broadcast(
                {
                    "type": "reading",
                    "data": result,
                    "stats": self.stats,
                }
            )

            # Acknowledge message
            await self.redis.xack(
                settings.redis_stream, settings.redis_group, msg_id
            )
        except Exception as e:
            print(f"[Consumer] process error: {e}")

    async def stop(self):
        self._running = False
        await self.redis.aclose()