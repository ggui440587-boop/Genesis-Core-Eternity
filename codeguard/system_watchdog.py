import subprocess
import time
import os

# ==============================================================
# System Watchdog Module - 系統看門狗與自動重啟守護進程
# ==============================================================

TARGET_SCRIPT = "main_ecosystem.py"

def run_watchdog():
    """啟動看門狗機制，持續監控主生態系並在當機時自動重啟"""
    print("=" * 60)
    print(" 🐕 [看門狗守護] 系統進程監控已啟動：隨時準備守護核心運作...")
    print("=" * 60)

    try:
        while True:
            if not os.path.exists(TARGET_SCRIPT):
                print(f"[看門狗警告] 找不到目標主程式 [{TARGET_SCRIPT}]，暫停監控...")
                time.sleep(5)
                continue

            print(f"[看門狗巡邏] 正在確認 [{TARGET_SCRIPT}] 運行狀態...")

            # 啟動主控生態系進程
            process = subprocess.Popen(["python", TARGET_SCRIPT])

            # 等待其運行，若進程結束則代表可能當機或被關閉
            process.wait()

            print(f"[看門狗警報] 偵測到 [{TARGET_SCRIPT}] 已停止運行！準備在 3 秒後自動重啟...")
            time.sleep(3)

    except KeyboardInterrupt:
        print("\n[看門狗關閉] 收到中斷訊號，守護進程安全退出。")

if __name__ == "__main__":
    run_watchdog()

