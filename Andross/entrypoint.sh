#!/bin/bash

if [ "$1" == "start" ]; then
    python3.10 -u main.py
elif [ "$1" == "shell" ]; then
    /bin/bash
else
    echo "Unknown command: $1"
    exit 1
fi
