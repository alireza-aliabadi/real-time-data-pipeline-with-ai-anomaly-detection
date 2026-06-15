"""Manages active WebSocket connections and broadcasting."""
import asyncio
import json
from fastapi import WebSocket


class WebSocketManager:
    def __init__(self):
        self.active: list[WebSocket] = []
        self._lock = asyncio.Lock()

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        async with self._lock:
            self.active.append(websocket)
        print(f"[WS] Client connected. Total: {len(self.active)}")

    async def disconnect(self, websocket: WebSocket):
        async with self._lock:
            if websocket in self.active:
                self.active.remove(websocket)
        print(f"[WS] Client disconnected. Total: {len(self.active)}")

    async def broadcast(self, message: dict):
        if not self.active:
            return
        payload = json.dumps(message)
        dead = []
        # snapshot to avoid mutation during iteration
        for ws in list(self.active):
            try:
                await ws.send_text(payload)
            except Exception:
                dead.append(ws)
        for ws in dead:
            await self.disconnect(ws)


ws_manager = WebSocketManager()