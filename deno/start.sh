#!/bin/bash
deno run --allow-net --allow-env mod.ts &
echo $! > server.pid