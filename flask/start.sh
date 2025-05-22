#!/bin/bash

source .venv/bin/activate

gunicorn -w 8 main:app -b :3000 &
echo $! > server.pid