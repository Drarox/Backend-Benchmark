#!/bin/bash
deno run --allow-net --allow-env main.ts &
echo $! > server.pid