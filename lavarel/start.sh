#!/bin/bash
php artisan octane:frankenphp --port=3000 &
echo $! > server.pid