#!/bin/bash

source .venv/bin/activate

# Detect number of CPU cores (logical)
CORES=$(getconf _NPROCESSORS_ONLN 2>/dev/null || getconf NPROCESSORS_ONLN 2>/dev/null || sysctl -n hw.ncpu 2>/dev/null)

# Calculate recommended number of workers: (2 x cores) + 1
WORKERS=$((CORES * 2 + 1))

# uvicorn djangobench.asgi:application --port 3000 --workers $WORKERS --log-level warning &
# echo $! > server.pid

# gunicorn -w $WORKERS --bind 0.0.0.0:3000 djangobench.wsgi &
# echo $! > server.pid

gunicorn djangobench.asgi:application -k uvicorn_worker.UvicornWorker -w $WORKERS --bind 0.0.0.0:3000 &
echo $! > server.pid