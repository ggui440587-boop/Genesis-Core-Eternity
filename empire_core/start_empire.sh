#!/bin/bash

echo "========================================================"
echo "👑 【帝國啟動令】正在召喚永生守護靈與皇帝核心..."
echo "========================================================"

if [ ! -f "core_engine.py" ]; then
    echo "[!] 查無 core_engine.py，請先建立帝國核心！"
    exit 1
fi

while true; do
    echo "[+] 🕒 [$(date)] 帝國核心正在運行中..."
    python core_engine.py
    
    echo "[!] ⚠️ [$(date)] 警告：帝國核心曾短暫歇息，守護靈正在執行緊急喚醒..."
    sleep 3
done

