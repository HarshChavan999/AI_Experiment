#!/usr/bin/env bash

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PID_FILE="${DIR}/overnight.pid"

if [ -f "$PID_FILE" ]; then
    PID=$(cat "$PID_FILE")
    if ps -p "$PID" > /dev/null 2>&1; then
        echo "Stopping overnight training process (PID: $PID)..."
        pkill -P "$PID" 2>/dev/null || true
        kill -15 "$PID" 2>/dev/null || true
        rm -f "$PID_FILE"
        echo "Process stopped safely."
    else
        echo "Process $PID is not running."
        rm -f "$PID_FILE"
    fi
else
    echo "No running overnight training process found."
fi

