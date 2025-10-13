<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;

class ProcessController extends Controller
{
    public function store(Request $request)
    {
        $numbers = $request->input('numbers', []);
        $sumOfSquares = collect($numbers)->map(function ($number) {
            return $number * $number;
        })->sum();

        return response()->json(['result' => $sumOfSquares]);
    }
}
