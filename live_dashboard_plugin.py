import time
import random
import os
import glob

class LiveDashboardPlugin:
    def __init__(self, refresh_interval=1.0):
        self.refresh_interval = refresh_interval
        print("-> 🔴 [即時面板] 動態數據串流面板初始化成功！準備進入即時監控...")
        time.sleep(1)

    def run_live_stream(self, max_frames=10):
        """以迴圈方式即時刷新數據，讓你看見數據真正跑起來"""
        for frame in range(1, max_frames + 1):
            # 清除終端機畫面
            os.system('cls' if os.name == 'nt' else 'clear')
            
            # 模擬即時變動的數據
            cpu_usage = round(random.uniform(15.0, 85.0), 1)
            mem_usage = round(random.uniform(40.0, 75.0), 1)
            active_threads = random.randint(2, 8)
            plugin_count = len(glob.glob("*_plugin.py"))

            print("=" * 50)
            print(f" 🚀 Termux 即時系統監控面板 (Frame: {frame}/{max_frames})")
            print("=" * 50)
            print(f" 🟢 系統狀態      : 運行中 (LIVE)")
            print(f" ⏱️ 當前時間      : {time.strftime('%H:%M:%S')}")
            print(f" 📦 活躍外掛數    : {plugin_count} 個")
            print(f" --------------------------------------------------")
            print(f" 🔥 CPU 即時負載  : [{self.get_bar(cpu_usage)}] {cpu_usage}%")
            print(f" 💾 記憶體佔用    : [{self.get_bar(mem_usage)}] {mem_usage}%")
            print(f" 🧵 執行緒池狀態  : {active_threads} 條執行緒運作中")
            print("=" * 50)
            print(" 💡 提示：數據正在即時跳動中... (按 Ctrl+C 可隨時終止)")
            
            time.sleep(self.refresh_interval)

    def get_bar(self, percent):
        """產生簡易的進度條圖示"""
        filled = int(percent / 10)
        return "█" * filled + "-" * (10 - filled)

if __name__ == "__main__":
    dashboard = LiveDashboardPlugin(refresh_interval=1.0)
    try:
        dashboard.run_live_stream(max_frames=15)
    except KeyboardInterrupt:
        print("\n-> 🛑 即時面板已手動終止。")
