#!/bin/bash
bun index.js &
echo $! > server.pid