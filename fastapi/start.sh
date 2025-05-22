#!/bin/bash

source .venv/bin/activate

uvicorn main:app --port 3000 --log-level warning &
echo $! > server.pid