#!/bin/bash

SERVER_URL="http://localhost:3000/ping"
LOG_FILE="/logs/health.log"

# Ensure log directory exists
mkdir -p "$(dirname "$LOG_FILE")"

echo "Starting health check for $SERVER_URL..."
echo "Logging failures to $LOG_FILE"

while true; do
    TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")

    if curl -fsS "$SERVER_URL" > /dev/null 2>&1; then
        echo "[$TIMESTAMP] OK"
    else
        echo "[$TIMESTAMP] HEALTH CHECK FAILED for $SERVER_URL" >> "$LOG_FILE"
    fi

    sleep 10
done
