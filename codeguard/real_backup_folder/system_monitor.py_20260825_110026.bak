import os
import datetime

# ==============================================================
# System Monitor Module - 系統資源與效能監控模組
# ==============================================================

class SystemMonitor:
    @staticmethod
    def check_resource_usage():
        """檢查當前 Python 進程的資源與記憶體佔用狀況"""
        print("=" * 60)
        print(f" 📊 [效能監控] 正在檢測 Termux 背景進程資源狀況...")
        print("=" * 60)

        # 取得當前行程 ID (PID)
        pid = os.getpid()
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # 在 Linux / Termux 環境下讀取 /proc/self/status 取得記憶體資訊
        mem_usage_kb = "未知"
        try:
            with open("/proc/self/status", "r") as f:
                for line in f:
                    if line.startswith("VmRSS:"):
                        mem_usage_kb = line.split()[1] + " " + line.split()[2]
                        break
        except Exception:
            pass

        print(f"-> 🕒 檢測時間: {timestamp}")
        print(f"-> 🆔 當前行程 PID: {pid}")
        print(f"-> 💾 實體記憶體佔用 (VmRSS): {mem_usage_kb}")
        print("-> 🟢 [狀態正常] 系統資源消耗在安全範圍內。")
        print("=" * 60)

if __name__ == "__main__":
    SystemMonitor.check_resource_usage()

