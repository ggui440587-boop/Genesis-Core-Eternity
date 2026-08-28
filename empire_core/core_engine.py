import os
import sqlite3
import importlib.util
import time
import random
from datetime import datetime

class ImmortalEmperorCore:
    def __init__(self, db_name="fusion_hub.db"):
        self.db_name = db_name
        self.dynasty_version = "v3.0-Eternal"
        self.init_imperial_archives()
        self.verify_succession()

    def init_imperial_archives(self):
        """初始化帝國的完整資料庫：涵蓋領土、爵位、商會、人民、奴隸、暗部、教會與編年史"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        # 1. 帝國編年史表（史官院記錄）
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS imperial_chronicles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                era_version TEXT,
                event_type TEXT,
                description TEXT,
                recorded_at TEXT
            )
        ''')
        
        # 2. 皇位繼承與核心意志表（永生協議）
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS imperial_succession (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                emperor_title TEXT UNIQUE,
                supreme_will TEXT,
                ascension_date TEXT
            )
        ''')

        # 3. 百官奏摺與元老院審查表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS senate_petitions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                department TEXT,
                report_content TEXT,
                status TEXT,
                submitted_at TEXT
            )
        ''')

        # 4. 暗部肅清與抄家紀錄表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS secret_police_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                target_module TEXT,
                crime_action TEXT,
                penalty TEXT,
                executed_at TEXT
            )
        ''')

        # 5. 資源、商會與資產表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS imperial_treasury (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                asset_name TEXT UNIQUE,
                quantity INTEGER,
                last_updated TEXT
            )
        ''')

        # 6. 拓荒領土、人民與奴隸表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS empire_domains (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                territory_name TEXT UNIQUE,
                ruler_title TEXT,
                citizens_count INTEGER,
                slaves_count INTEGER,
                status TEXT,
                annexed_at TEXT
            )
        ''')

        # 7. 天災與危機紀錄表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS imperial_cataclysms (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                crisis_name TEXT,
                severity TEXT,
                resolved_status TEXT,
                triggered_at TEXT
            )
        ''')

        conn.commit()
        conn.close()

    def verify_succession(self):
        """皇位繼承與永生驗證：確保皇帝意志不滅"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        cursor.execute('''
            INSERT OR IGNORE INTO imperial_succession (emperor_title, supreme_will, ascension_date)
            VALUES (?, ?, ?)
        ''', ("Supreme Emperor of Termux", "Absolute Obedience & Infinite Expansion", now))
        
        cursor.execute('''
            INSERT INTO imperial_chronicles (era_version, event_type, description, recorded_at)
            VALUES (?, ?, ?, ?)
        ''', (self.dynasty_version, "SUCCESSION", "皇帝核心意志完成驗證，永生大統正式啟動。", now))
        
        conn.commit()
        conn.close()
        print("👑 【皇位永生驗證】皇帝至高意志已鎖定於核心資料庫，萬世永存。")

    def log_chronicle(self, event_type, description):
        """史官院記錄重大歷史"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute('''
            INSERT INTO imperial_chronicles (era_version, event_type, description, recorded_at)
            VALUES (?, ?, ?, ?)
        ''', (self.dynasty_version, event_type, description, now))
        conn.commit()
        conn.close()

    def simulate_cataclysm_or_prosperity(self):
        """天災與外患危機隨機模擬系統"""
        events = [
            ("None", "帝國風調雨順，資料庫脈動平穩。"),
            ("Digital Dust Storm", "邊境遭遇數位沙塵暴（網路延遲或 API 波動），後勤部已緊急修復。"),
            ("Merchant Guild Boom", "東部商會開闢新航路，帝國財政獲得顯著盈餘。"),
            ("Minor Heresy", "基層出現未授權的微小錯誤修改，暗部已迅速介入肅清。")
        ]
        chosen_crisis, desc = random.choice(events)
        if chosen_crisis != "None":
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            cursor.execute('''
                INSERT INTO imperial_cataclysms (crisis_name, severity, resolved_status, triggered_at)
                VALUES (?, ?, ?, ?)
            ''', (chosen_crisis, "Moderate", "RESOLVED_BY_EMPIRE", now))
            conn.commit()
            conn.close()
            print(f"⚡ [天災警報] 偵測到外患危機：{desc}")
            self.log_chronicle("CATACLYSM", f"化解危機：{chosen_crisis} - {desc}")
        else:
            print(f"✨ [國泰民安] {desc}")

    def hold_grand_assembly(self, plugin_dir="plugins"):
        """皇帝陛下召開全功能大朝會"""
        if not os.path.exists(plugin_dir):
            os.makedirs(plugin_dir)

        print("\n========================================================")
        print(f"👑 【皇帝陛下登朝】當前時代：{self.dynasty_version}")
        print("========================================================")
        
        # 1. 抽檢天災與危機
        self.simulate_cataclysm_or_prosperity()

        # 2. 召集各部門外掛臣屬
        discovered_modules = []
        for filename in os.listdir(plugin_dir):
            if filename.endswith(".py") and not filename.startswith("__"):
                module_name = filename[:-3]
                file_path = os.path.join(plugin_dir, filename)
                try:
                    spec = importlib.util.spec_from_file_location(module_name, file_path)
                    mod = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(mod)
                    tier = getattr(mod, "TIER", 3)
                    discovered_modules.append((tier, module_name, mod))
                except Exception as e:
                    print(f"[!] 臣屬外掛載入異常 {module_name}: {e}")

        # 依階級排序執行朝會
        discovered_modules.sort(key=lambda x: x[0])

        for tier, module_name, mod in discovered_modules:
            try:
                if hasattr(mod, "run"):
                    print(f"\n--- [召見階級 T{tier}] 聽取 【{module_name.upper()}】 奏摺 ---")
                    mod.run(self.db_name)
                    self.log_chronicle("DEPT_REPORT", f"部門 {module_name} (T{tier}) 順利完成朝會述職。")
                else:
                    print(f"[-] 臣屬 {module_name} 無法對外奏報 (缺少 run 方法)")
            except Exception as e:
                print(f"[!] [肅清警報] 臣屬 {module_name} 發生錯誤: {e}")
                self.log_chronicle("REBEL_ERROR", f"部門 {module_name} 發生嚴重錯誤，暗部已記錄：{e}")

        print("\n--------------------------------------------------------")
        print("📜 【史官院】本輪朝會政務與歷史軌跡已全數編纂入檔。")
        print("========================================================")

if __name__ == "__main__":
    print("=== 🏛️ 不朽數位帝國主機啟動：皇帝坐鎮中樞 ===")
    emperor = ImmortalEmperorCore()
    
    while True:
        emperor.hold_grand_assembly()
        print("[-] 皇城暫歇，帝國進入 24/7 背景自治永動循環，60秒後再次面聖...\n")
        time.sleep(60)

