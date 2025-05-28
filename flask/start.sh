#!/bin/bash

source .venv/bin/activate

# Detect number of CPU cores (logical)
CORES=$(getconf _NPROCESSORS_ONLN 2>/dev/null || getconf NPROCESSORS_ONLN 2>/dev/null || sysctl -n hw.ncpu 2>/dev/null)

# Calculate recommended number of workers: (2 x cores) + 1
WORKERS=$((CORES * 2 + 1))

gunicorn -w $WORKERS -k gevent main:app -b :3000 &
echo $! > server.pid