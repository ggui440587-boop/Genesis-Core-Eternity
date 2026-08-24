import asyncio
import importlib
import os
import logging
import sqlite3
from dotenv import load_dotenv
from plugins.base import BasePlugin

# 載入安全環境變數
load_dotenv()

# 設定本地日誌與安全目錄
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    filename="logs/system_audit.log",
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class SecureSystemManager:
    def __init__(self):
        self.plugins = []
        self._init_local_db()
        self._load_plugins()

    def _init_local_db(self):
        """建立完全獨立於雲端的本地 SQLite 資料庫，確保資料安全"""
        with sqlite3.connect("secure_local_audit.db") as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS local_ledger (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT,
                    event_status TEXT
                )
            """)

    def _load_plugins(self):
        """自動動態擴充載入 plugins 目錄下的所有模組"""
        plugin_dir = "plugins"
        for filename in os.listdir(plugin_dir):
            if filename.endswith("_plugin.py"):
                module_name = f"plugins.{filename[:-3]}"
                try:
                    module = importlib.import_module(module_name)
                    if hasattr(module, "Plugin"):
                        self.plugins.append(module.Plugin())
                        print(f"🛡️ 成功安全載入擴充插件: {module_name}")
                except Exception as e:
                    print(f"⚠️ 插件載入異常 ({module_name}): {e}")

    async def run(self):
        print("🚀 【安全防護·自動擴充生產系統】已在本地正式啟動！")
        while True:
            tasks = []
            for plugin in self.plugins:
                # 包裹防護：確保單一插件崩潰不會影響全局
                async def safe_run(p):
                    try:
                        await asyncio.wait_for(p.execute(), timeout=10)
                    except Exception as e:
                        print(f"🔥 攔截到插件異常，系統已自動隔離: {e}")
                tasks.append(safe_run(plugin))
            
            await asyncio.gather(*tasks, return_exceptions=True)
            
            # 隨機化間隔 (60 ~ 120 秒)，保護免費額度、避免被雲端 API 封鎖
            sleep_time = 60
            await asyncio.sleep(sleep_time)

if __name__ == "__main__":
    if not os.path.exists(".env"):
        print("❌ 錯誤：找不到安全設定檔 .env！請先建立並配置金鑰。")
    else:
        manager = SecureSystemManager()
        try:
            asyncio.run(manager.run())
        except (KeyboardInterrupt, SystemExit):
            print("\n🛑 系統已安全關閉，所有本地數據與資料庫均受保護且完好無缺。")

