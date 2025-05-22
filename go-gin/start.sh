#!/bin/bash
export GIN_MODE=release

go build -o server main.go
./server & 
echo $! > server.pid