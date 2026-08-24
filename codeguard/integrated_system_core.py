import time
import datetime
import threading

# 匯入先前建構的核心模組
from system_config import load_config
from event_bus import EventBus
from garbage_collector import SystemGarbageCollector

# ==============================================================
# Integrated System Core with Autonomous Cycle & Sleep
# 具備自主循環與智慧休眠的全系統整合核心
# ==============================================================

class GenesisIntegratedCore:
    def __init__(self):
        self.config = load_config()
        self.event_bus = EventBus()
        self.is_running = True
        self.idle_counter = 0  # 紀錄連續無任務的次數（用於判斷是否該睡覺）

    def autonomous_sleep_cycle(self):
        """自主循環與智慧休眠機制 (背景執行緒)"""
        print("[整合核心] 🔄 自主循環與休眠調度中心已啟動...")

        while self.is_running:
            current_hour = datetime.datetime.now().hour

            # 模擬智慧休眠判斷：例如深夜時段 (假設 0 點到 6 點) 或連續閒置過久，系統自動進入深層睡眠
            is_night_time = (0 <= current_hour < 6)

            if is_night_time or self.idle_counter > 5:
                sleep_time = 15  # 進入深層睡眠，拉長心跳間隔以節省資源
                print(f"-> [系統休眠] 💤 當前處於低負載或夜間時段，心跳放緩，休眠 {sleep_time} 秒...")
            else:
                sleep_time = self.config.get("heart_rate_seconds", 5)
                print(f"-> [自主循環] ⚡ 系統維持正常活躍狀態，循環間隔 {sleep_time} 秒。")

            # 廣播自主循環事件
            self.event_bus.publish("AUTONOMOUS_PULSE", f"系統自主運行中 (閒置計數: {self.idle_counter})")

            self.idle_counter += 1
            time.sleep(sleep_time)

    def start_all_systems(self):
        """啟動並串聯所有身體部位與自主循環"""
        print("=" * 60)
        print(f" 🚀 啟動具備自主循環與休眠機制的生態系")
        print("=" * 60)

        # 啟動自主循環與休眠背景執行緒
        cycle_thread = threading.Thread(target=self.autonomous_sleep_cycle, daemon=True)
        cycle_thread.start()

        print("[整合核心] 🟢 自主循環與休眠機制已上線！(按 Ctrl + C 停止)")

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n[整合核心] 收到關閉指令，自主生態系安全停止運作。")

if __name__ == "__main__":
    core = GenesisIntegratedCore()
    core.start_all_systems()

