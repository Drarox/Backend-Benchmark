#!/bin/bash
bun src/index.ts &
echo $! > server.pid