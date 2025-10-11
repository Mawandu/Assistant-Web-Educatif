# backend/Dockerfile

FROM python:3.12-slim

WORKDIR /app
RUN apt-get update && apt-get install -y netcat-openbsd && rm -rf /var/lib/apt/lists/*
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY backend/ .
COPY scripts/ ./scripts/

COPY backend/entrypoint.sh .
RUN chmod +x ./entrypoint.sh
#ENV PYTHONPATH="/app"
ENTRYPOINT ["./entrypoint.sh"]