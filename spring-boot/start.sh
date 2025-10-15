#!/bin/bash

java -jar build/libs/spring-boot-0.0.1-SNAPSHOT.jar &
echo $! > server.pid