FROM python:3.14.6-slim

WORKDIR /app

# System deps for scikit-learn/numpy
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc g++ && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml ./
RUN python -c "import tomllib; deps = tomllib.load(open('pyproject.toml', 'rb'))['project']['dependencies']; print('\\n'.join(deps))" > requirements.txt \
    && pip install --no-cache-dir -r requirements.txt

COPY app ./app

# Train the model at build time so it's ready
RUN python -m app.ml.train

EXPOSE 8000

# Note: with the in-process producer/consumer design, use 1 worker.
# For multi-worker, externalize producer/consumer into separate services.
# uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 1
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]