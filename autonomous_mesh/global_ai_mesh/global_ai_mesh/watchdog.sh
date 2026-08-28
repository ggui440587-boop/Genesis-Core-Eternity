#!/bin/bash
while true; do
    echo "[Watchdog] 檢查 Genesis-Core 守護進程狀態..."
    if ! pgrep -f "server.py" > /dev/null; then
        echo "[Watchdog] 偵測到伺服器中斷，正在自動復活..."
        python server.py &
    fi
    sleep 10
done
