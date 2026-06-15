"""FastAPI app: orchestrates producer, consumer, and WebSocket server."""
import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware

from app.pipeline.producer import DataProducer
from app.pipeline.consumer import StreamConsumer
from app.ws.manager import ws_manager
from app.ml.train import main as retrain_model

producer = DataProducer()
consumer = StreamConsumer()
background_tasks: list[asyncio.Task] = []


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: launch producer + consumer as background tasks
    print("[App] Starting background pipeline...")
    background_tasks.append(asyncio.create_task(producer.start()))
    background_tasks.append(asyncio.create_task(consumer.start()))
    yield
    # Shutdown
    print("[App] Shutting down pipeline...")
    await producer.stop()
    await consumer.stop()
    for task in background_tasks:
        task.cancel()
    await asyncio.gather(*background_tasks, return_exceptions=True)


app = FastAPI(title="Realtime Anomaly Pipeline", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],  # replace wildcard
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

@app.get("/health")
async def health():
    return {"status": "ok", "stats": consumer.stats}

@app.get("/stats")
async def stats():
    return consumer.stats

@app.post("/admin/retrain")
async def retrain(background_tasks: BackgroundTasks):
    """Trigger model retraining without downtime."""
    background_tasks.add_task(retrain_model)
    return {"status": "retraining started"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await ws_manager.connect(websocket)
    try:
        while True:
            # keep connection alive; ignore incoming client msgs
            await websocket.receive_text()
    except WebSocketDisconnect:
        await ws_manager.disconnect(websocket)
    except Exception:
        await ws_manager.disconnect(websocket)