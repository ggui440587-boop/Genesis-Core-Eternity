import os
import sqlite3
import subprocess
import difflib

class MatrixVectorImmuneCore:
    def __init__(self, db_name="matrix_intel.db"):
        self.db_name = db_name
        print("[Immune-Pure-Core] 正在初始化輕量級純 Python 智慧檢索大腦與免疫防禦網...")
        self.init_vector_table()

    def init_vector_table(self):
        """在 SQLite 中建立智庫索引表"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS vector_vault (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source_id INTEGER,
                content TEXT,
                category TEXT
            )
        """)
        conn.commit()
        conn.close()

    def sync_sqlite_to_vector(self):
        """將 SQLite 智庫的新情報同步至檢索核心"""
        print("[Vector Sync] 正在同步智庫索引...")
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT id, title, category FROM intel_vault")
        rows = cursor.fetchall()

        added_count = 0
        for row_id, title, category in rows:
            cursor.execute("SELECT id FROM vector_vault WHERE source_id = ?", (row_id,))
            if not cursor.fetchone():
                cursor.execute(
                    "INSERT INTO vector_vault (source_id, content, category) VALUES (?, ?, ?)",
                    (row_id, title, category)
                )
                added_count += 1
                
        conn.commit()
        conn.close()
        print(f"[✅ 智庫同步] 成功同步 {added_count} 筆新情報至純 Python 智慧大腦！")

    def semantic_search(self, query, top_k=3):
        """利用純 Python 模糊匹配與關鍵字交集進行智慧檢索"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT content, category FROM vector_vault")
        rows = cursor.fetchall()
        conn.close()

        if not rows:
            print("[❌ 檢索] 智庫目前為空。")
            return

        scored_results = []
        for content, category in rows:
            # 計算字串相似度分數 (0 到 1 之間)
            match_ratio = difflib.SequenceMatcher(None, query.lower(), content.lower()).quick_ratio()
            # 如果查詢詞直接包含在內，給予額外加權
            if query.lower() in content.lower():
                match_ratio += 0.5
            scored_results.append((match_ratio, content, category))

        # 依分數排序
        scored_results.sort(key=lambda x: x[0], reverse=True)

        print(f"\n=== 🧠 智慧語意模糊檢索報告 (查詢: '{query}') ===")
        for idx, (score, content, category) in enumerate(scored_results[:top_k], 1):
            print(f"{idx}. [匹配度: {score:.2f}] [{category}] {content}")
        print("================================================\n")

    def self_healing_watchdog(self):
        """自動化資安與免疫防禦機制（Self-Healing）"""
        print("[Immune Watchdog] 正在執行系統健康度與背景守衛掃描...")
        res = subprocess.run("termux-wake-lock", shell=True, capture_output=True)
        if res.returncode == 0:
            print("[🛡️ 免疫系統] 硬體防護正常：喚醒鎖（WakeLock）持續運作中。")
        else:
            print("[⚠️ 免疫警報] 發現硬體防護失效，正在自動重新加固...")
            subprocess.run("termux-wake-lock", shell=True)

        if os.path.exists(self.db_name):
            try:
                conn = sqlite3.connect(self.db_name)
                cursor = conn.cursor()
                cursor.execute("PRAGMA integrity_check;")
                status = cursor.fetchone()[0]
                conn.close()
                if status == "ok":
                    print("[🛡️ 免疫系統] 資料庫結構完整性：100% 正常。")
                else:
                    print("[❌ 免疫危機] 資料庫偵測到異常損壞！")
            except Exception as e:
                print(f"[❌ 免疫例外] {e}")

    def run_immune_cycle(self):
        self.self_healing_watchdog()
        self.sync_sqlite_to_vector()

if __name__ == "__main__":
    core = MatrixVectorImmuneCore()
    core.run_immune_cycle()
    core.semantic_search("AI")

