#!/bin/bash
dotnet run --project . --urls http://0.0.0.0:3000 &
echo $! > server.pid