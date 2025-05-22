#!/bin/bash
go build -o server main.go
./server & 
echo $! > server.pid