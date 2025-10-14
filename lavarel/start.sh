#!/bin/bash
php artisan octane:frankenphp --port=3000 --workers=auto --log-level=warn &
echo $! > server.pid