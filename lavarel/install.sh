#!/bin/bash

composer update

composer install

php artisan octane:install --server=frankenphp