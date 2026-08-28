#!/bin/bash

echo "-> 🚀 [啟動腳本] 正在準備啟動 Termux 矩陣自動化工廠..."

# 1. 確保手機背景保持喚醒狀態（防止休眠中斷）
if command -v termux-wake-lock &> /dev/null; then
    termux-wake-lock
    echo "-> 🔋 [系統] 已成功啟用 Termux 喚醒鎖定 (WakeLock)。"
else
    echo "-> ℹ️ [系統] 未檢測到 Termux API，跳過喚醒鎖定。"
fi

# 2. 檢查主控制器是否存在
if [ ! -f "main_controller.py" ]; then
    echo "-> ❌ [錯誤] 找不到 main_controller.py 主控制器檔案！"
    exit 1
fi

echo "-> 💡 [系統] 正在載入十六大外掛完全體，按 Ctrl + C 可隨時安全終止..."

# 3. 執行 Python 主控制器
python main_controller.py
