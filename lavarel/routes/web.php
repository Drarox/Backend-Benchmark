<?php

use Illuminate\Support\Facades\Route;
use App\Http\Controllers\ProcessController;

Route::get('/', function () {
    return view('welcome');
});

Route::post('/process', [ProcessController::class, 'store']);
