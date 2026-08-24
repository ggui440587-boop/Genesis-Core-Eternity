import asyncio
import datetime
from config_loader import ConfigLoader
from database_logger import DatabaseLogger

# ==============================================================
# Ultimate Ecosystem Daemon - 終極生態系守護主控與日誌串聯模組
# ==============================================================

class UltimateEcosystemDaemon:
    def __init__(self):
        # 1. 載入全域設定
        self.config = ConfigLoader.load_config()
        self.is_running = True
        self.cycle_count = 0

    async def execute_eternal_cycle(self):
        """啟動包含資料庫記錄與非同步心跳的完整生命週期迴圈"""
        print("=" * 65)
        print(f" 🚀 [終極主控] 啟動 [{self.config['app_name']}] 全模組串聯守護進程...")
        print(f" 執行環境: {self.config['environment']} | 除錯模式: {self.config['debug_mode']}")
        print(f" 提示: 在 Termux 中若要停止運行，請隨時按下 [Ctrl + C]")
        print("=" * 65)

        # 初始化資料庫日誌表
        DatabaseLogger.init_database()
        DatabaseLogger.log_level = "INFO"

        try:
            while self.is_running:
                self.cycle_count += 1
                current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                # 模擬心跳脈搏與狀態訊息
                log_msg = f"生態系心跳循環 #{self.cycle_count} 運行正常。時間: {current_time}"
                print(f"💓 [{current_time}] {log_msg}")

                # 將事件同步寫入 SQLite 資料庫持久化保存
                DatabaseLogger.log_event("INFO", log_msg)

                print("-" * 65)
                # 根據設定或預設間隔 3 秒進行下一次循環
                await asyncio.sleep(3)

        except asyncio.CancelledError:
            print("🛑 [終極主控] 收到停止訊號，正在安全關閉所有背景進程...")
            DatabaseLogger.log_event("WARNING", "終極生態系守護進程被手動中斷關閉。")

if __name__ == "__main__":
    daemon = UltimateEcosystemDaemon()
    try:
        asyncio.run(daemon.execute_eternal_cycle())
    except KeyboardInterrupt:
        print("\n✨ [安全退出] 終極生態系主控腳本已成功停止運行！")

