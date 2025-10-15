#!/bin/bash
set -e

composer update

composer install

php artisan octane:install --server=frankenphp