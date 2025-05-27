#!/bin/bash
npm run build
node dist/main &
echo $! > server.pid