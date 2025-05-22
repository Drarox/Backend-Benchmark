#!/bin/bash
deno run --allow-net mod.ts &
echo $! > server.pid