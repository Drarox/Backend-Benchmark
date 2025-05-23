#!/bin/bash

source .venv/bin/activate

gunicorn -w 16 -k gevent main:app -b :3000 &
echo $! > server.pid