import sqlite3
import datetime

# ==============================================================
# System Study & Learning Module - 數位知識閱讀與自動化學習模組
# ==============================================================

DB_NAME = "study_knowledge_base.db"

class StudyLearningModule:
    def __init__(self):
        self.init_study_table()

    def init_study_table(self):
        """初始化學習筆記資料庫表格"""
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS study_notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                topic TEXT NOT NULL,
                summary TEXT NOT NULL,
                status TEXT DEFAULT 'COMPLETED',
                studied_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        conn.close()
        print("[學習系統] 知識資料庫初始化完成，準備好隨時讀書充電！")

    def record_study_session(self, topic, summary):
        """記錄一筆新的讀書筆記與學習心得"""
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO study_notes (topic, summary) VALUES (?, ?)",
            (topic, summary)
        )
        conn.commit()
        conn.close()
        print("=" * 50)
        print(f" 📚 [讀書動起來] 成功完成學習主題: [{topic}]")
        print(f"    摘要筆記: {summary}")
        print("=" * 50)

if __name__ == "__main__":
    learner = StudyLearningModule()
    learner.record_study_session(
        "Python 模組化架構與非同步執行", 
        "深入理解了執行緒 (Threading) 與事件匯流排的運作原理，能有效避免多工衝突。"
    )

