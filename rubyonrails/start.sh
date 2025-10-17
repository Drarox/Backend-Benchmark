#!/bin/bash

rails server -e production &
echo $! > server.pid
