#!/bin/bash

# Check if requirements.txt exists
if [ ! -f requirements.txt ]; then
    echo "requirements.txt not found!"
    exit 1

# Install the dependencies from requirements.txt
pip install -r requirements.txt

cd rurl_flow

crewai install

echo "Dependencies installed successfully."