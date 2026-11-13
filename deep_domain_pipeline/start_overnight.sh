#!/usr/bin/env bash
set -e

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PID_FILE="${DIR}/overnight.pid"
LOG_FILE="${DIR}/overnight_training.log"
PYTHON_BIN="/Users/harshchavan/qwen_finetune_experiment/.venv/bin/python3"

if [ -f "$PID_FILE" ]; then
    PID=$(cat "$PID_FILE")
    if ps -p "$PID" > /dev/null 2>&1; then
        echo "Overnight training is ALREADY running with PID: $PID"
        echo "Use './check_progress.sh' to view progress."
        exit 1
    fi
fi

echo "======================================================================"
echo " Starting Overnight M4 Deep Domain Training Pipeline (12,000 Samples) "
echo "======================================================================"
echo "• Target Hardware: Apple M4 (utilizing 8-10 GB unified memory)"
echo "• Prevent Sleep: Enabled via macOS 'caffeinate'"
echo "• Output Log: ${LOG_FILE}"
echo "======================================================================"

# caffeinate: -d (prevent display sleep), -i (prevent idle sleep), -s (prevent system sleep on AC)
nohup caffeinate -dis "${PYTHON_BIN}" "${DIR}/orchestrate_overnight.py" >> "${LOG_FILE}" 2>&1 &
PID=$!
echo $PID > "$PID_FILE"

echo "Pipeline launched in background with PID: $PID"
echo "You can close this terminal. To check status anytime, run:"
echo "  ${DIR}/check_progress.sh"
echo "======================================================================"

