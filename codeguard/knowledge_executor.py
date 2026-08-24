import sqlite3
from action_module import ActionModule

# ==============================================================
# Knowledge Executor Module - 知識轉化與行動執行模組 (連結讀書與動起來)
# ==============================================================

class KnowledgeExecutor:
    def __init__(self):
        self.db_name = "knowledge_base.db"
        self.action_runner = ActionModule()

    def execute_latest_knowledge(self):
        """讀取資料庫中最 recentes 的知識，並讓系統動起來執行"""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute("SELECT topic, content FROM study_records ORDER BY id DESC LIMIT 1")
            row = cursor.fetchone()
            conn.close()

            if row:
                topic, content = row
                print("=" * 60)
                print(f" 🧠 [知識轉化] 成功提取讀書成果: [{topic}]")
                print(f"    內容摘要: {content}")
                print("=" * 60)

                # 將讀書學到的內容轉化為實際動作
                task_description = f"根據知識「{topic}」進行實作部署與運算"
                self.action_runner.start_moving(task_description)
            else:
                print("[知識警告] 知識庫中目前沒有任何記錄，請先進行讀書模組！")
        except Exception as e:
            print(f"[執行錯誤] 無法讀取知識庫: {e}")

if __name__ == "__main__":
    executor = KnowledgeExecutor()
    executor.execute_latest_knowledge()

