import sqlite3

# ==============================================================
# Study Module - 專責「讀書」與知識吸收模組
# ==============================================================

class StudyModule:
    def __init__(self):
        self.db_name = "knowledge_base.db"
        self._init_db()

    def _init_db(self):
        """初始化知識資料庫"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS study_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                topic TEXT NOT NULL,
                content TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()

    def read_and_absorb(self, topic, content):
        """專注於讀書與吸收知識，將內容存入知識庫"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO study_records (topic, content) VALUES (?, ?)", (topic, content))
        conn.commit()
        conn.close()
        print(f"📖 [讀書中] 成功吸收新知識：[{topic}] -> {content}")

if __name__ == "__main__":
    study = StudyModule()
    study.read_and_absorb("Python 基礎語法", "理解了類別與物件導向的獨立分工概念。")

