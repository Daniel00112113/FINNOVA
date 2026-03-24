FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias del sistema necesarias para xgboost/lightgbm
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
COPY requirements-pro.txt .

# Instalar requirements base + pro en un solo paso
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir xgboost lightgbm psycopg2-binary tqdm || true

COPY . .

EXPOSE 8000

CMD uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}
