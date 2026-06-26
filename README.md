# Real-Time Data Pipeline with AI Anomaly Detection

A real-time data processing pipeline that detects anomalies in sensor data using machine learning. Built with FastAPI, Redis Streams, and scikit-learn's IsolationForest algorithm.

## Architecture

```
┌─────────────┐      ┌─────────────┐      ┌─────────────┐      ┌─────────────┐
│  Producer   │────▶│   Redis     │────▶│  Consumer   │────▶│  Frontend   │
│ (Data Gen)  │      │   Stream    │      │ (Anomaly    │      │ (WebSocket) │
└─────────────┘      └─────────────┘      │  Detection) │      └─────────────┘
                                          └─────────────┘
                                                 │
                                                 ▼
                                          ┌───────────────┐
                                          │IsolationForest│
                                          │     Model     │
                                          └───────────────┘
```

## Tech Stack

### Backend
- **FastAPI** - Web framework and WebSocket server
- **Redis Streams** - Real-time data streaming
- **scikit-learn** - ML library (IsolationForest for anomaly detection)
- **NumPy/Pandas** - Data processing
- **Uvicorn** - ASGI server

### Frontend
- **React** (via Vite) - Real-time dashboard
- **WebSocket** - Live data updates

### Infrastructure
- **Docker & Docker Compose** - Containerization
- **Redis** - In-memory data store

## Features

- **Real-time anomaly detection** using IsolationForest algorithm
- **CPU-efficient ML model** (no GPU required)
- **WebSocket streaming** for live dashboard updates
- **Hot model retraining** without downtime
- **Resource-optimized** for low-spec hardware
- **Synthetic data generation** for testing

## Quick Start

### Prerequisites
- Docker and Docker Compose
- Python 3.14+ (for local development)

### Using Docker Compose (Recommended)

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

Services will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- Redis: localhost:6379

### Local Development

#### Backend Setup
```bash
cd backend

# Install dependencies
poetry install

# Train initial model
python -m app.ml.train

# Run backend
poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Run frontend
npm run dev
```

#### Redis Setup
```bash
# Using Docker
docker run -d -p 6379:6379 redis:8.8.0-alpine

# Or install locally
# See: https://redis.io/docs/latest/operate/oss_and_stack/install/install-redis/
```

## Configuration

Backend configuration is managed via environment variables or `.env` file:

| Variable | Default | Description |
|----------|---------|-------------|
| `REDIS_HOST` | localhost | Redis server host |
| `REDIS_PORT` | 6379 | Redis server port |
| `REDIS_STREAM` | sensor_stream | Redis stream name |
| `REDIS_GROUP` | anomaly_group | Consumer group name |
| `REDIS_CONSUMER` | consumer_1 | Consumer name |
| `CONTAMINATION` | 0.02 | Expected anomaly fraction (2%) |
| `FEATURE_WINDOW` | 10 | Rolling window size for features |
| `PRODUCE_INTERVAL_MS` | 200 | Data generation interval (5 msgs/sec) |

## API Endpoints

### Health Check
```bash
GET /health
```
Returns service status and consumer statistics.

### Statistics
```bash
GET /stats
```
Returns detailed pipeline statistics.

### Retrain Model
```bash
POST /admin/retrain
```
Triggers model retraining in the background without downtime.

### WebSocket
```bash
WS /ws
```
WebSocket endpoint for real-time anomaly data streaming.

## How Anomaly Detection Works

### Model: IsolationForest
- **Algorithm**: Unsupervised anomaly detection using random forest
- **Hardware**: CPU-based (2 cores), RAM-loaded
- **Training**: Synthetic normal data (temperature, vibration, pressure)
- **Inference**: Real-time prediction with anomaly scores

### Data Flow
1. **Producer** generates synthetic sensor data every 200ms
2. Data is pushed to **Redis Stream**
3. **Consumer** reads from stream using consumer group
4. **IsolationForest model** predicts anomalies (-1 = anomaly, 1 = normal)
5. Results are broadcast via **WebSocket** to frontend
6. **Frontend** displays real-time dashboard with anomaly alerts

### Model Parameters
- `n_estimators=100` - Number of trees in forest
- `contamination=0.02` - Expected 2% anomalies
- `max_samples=256` - Memory-efficient sampling
- `n_jobs=2` - Uses 2 CPU cores for parallelization

## Project Structure

```
.
├── backend/
│   ├── app/
│   │   ├── ml/
│   │   │   ├── model.py      # AnomalyModel class
│   │   │   └── train.py      # Model training script
│   │   ├── pipeline/
│   │   │   ├── producer.py   # Data generation
│   │   │   └── consumer.py   # Stream processing
│   │   ├── ws/
│   │   │   └── manager.py    # WebSocket manager
│   │   ├── config.py         # Configuration
│   │   └── main.py           # FastAPI app
│   ├── pyproject.toml        # Python dependencies
│   └── Dockerfile
├── frontend/
│   ├── src/                  # React source
│   ├── package.json
│   └── Dockerfile
├── docker-compose.yml
└── README.md
```

## Development

### Adding New Features
- **New metrics**: Modify `producer.py` and update model features
- **Model tuning**: Adjust parameters in `model.py` and retrain
- **Frontend updates**: Edit React components in `frontend/src/`

### Testing
```bash
# Backend tests
cd backend
poetry run pytest
```

## Performance

- **Memory**: < 1GB for backend, 256MB for frontend, 300MB for Redis
- **CPU**: 2 cores for backend, 0.5 cores for frontend
- **Latency**: Sub-second anomaly detection
- **Throughput**: 5 messages/second (configurable)