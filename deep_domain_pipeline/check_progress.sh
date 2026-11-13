#!/usr/bin/env bash

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PID_FILE="${DIR}/overnight.pid"
LOG_FILE="${DIR}/overnight_training.log"

echo "======================================================================"
echo " Overnight M4 Training Status & Progress "
echo "======================================================================"

if [ -f "$PID_FILE" ]; then
    PID=$(cat "$PID_FILE")
    if ps -p "$PID" > /dev/null 2>&1; then
        echo "Status: RUNNING (PID: $PID)"
        ps -o pid,%cpu,%mem,time,command -p "$PID"
    else
        echo "Status: COMPLETED or STOPPED (PID $PID is not running)"
    fi
else
    echo "Status: NOT STARTED"
fi

echo "----------------------------------------------------------------------"
echo "Recent Training Activity:"
if [ -f "$LOG_FILE" ]; then
    tail -n 15 "$LOG_FILE"
else
    echo "No log file found at ${LOG_FILE}"
fi
echo "======================================================================"

