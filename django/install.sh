#!/bin/bash
set -e

if [ -d ".venv" ]; then
    echo "Virtual environment .venv already exists."
else
    python3 -m venv .venv
fi

source .venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt
