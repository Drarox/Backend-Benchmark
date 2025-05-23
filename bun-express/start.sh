#!/bin/bash
bun index.ts &
echo $! > server.pid