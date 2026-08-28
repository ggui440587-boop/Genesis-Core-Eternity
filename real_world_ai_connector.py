import queue
import threading
import time
import datetime
import sqlite3
import logging
import requests
import json

# 設定系統日誌格式
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] ⚡ [真實 API 大腦]: %(message)s"
)

class RealAPIBrain:
    """串接真實世界 AI API 的大腦模組"""
    def __init__(self, api_key):
        self.api_key = api_key
        self.api_url = "https://api.groq.com/openai/v1/chat/completions"

    def query_llm(self, prompt):
        logging.info(f"🧠 [Groq 大腦] 正在透過真實 API 發送推理請求...")

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "llama-3.3-70b-versatile",
            "messages": [
                {"role": "system", "content": "你是一個世界級的程式開發與 AI 系統夥伴。"},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7
        }

        try:
            response = requests.post(self.api_url, headers=headers, json=payload, timeout=10)
            if response.status_code == 200:
                result_json = response.json()
                answer = result_json['choices'][0]['message']['content']
                return f"API 推理成功: {answer.strip()}"
            else:
                return f"API 錯誤代碼 {response.status_code}: {response.text}"
        except Exception as e:
            return f"連線例外狀況: {e}"

class WorldClassEngineWithAPI:
    """結合世界級訊息佇列與真實 API 大腦的總成系統"""
    def __init__(self, api_key, db_name="real_api_system.db"):
        self.db_name = db_name
        self.init_database()
        self.task_queue = queue.Queue()
        self.is_running = True

        # 初始化真實 API 大腦
        self.brain = RealAPIBrain(api_key)
        logging.info("真實 API 總成引擎初始化完成。")

    def init_database(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS api_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                prompt TEXT,
                response TEXT
            )
        ''')
        conn.commit()
        conn.close()

    def submit_prompt(self, prompt):
        self.task_queue.put(prompt)
        logging.info(f"⚡ 成功派發推理任務 -> {prompt}")

    def worker_node(self, worker_id):
        logging.info(f"⚙️ 工作節點 [{worker_id}] 已上線。")
        while self.is_running:
            try:
                prompt = self.task_queue.get(timeout=1.0)
            except queue.Empty:
                continue

            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logging.info(f"[{worker_id}] 正在處理提示詞: {prompt}")

            # 呼叫真實 API 取得 AI 回應
            ai_reply = self.brain.query_llm(prompt)

            # 寫入 SQLite 資料庫持久化
            self.save_record(timestamp, prompt, ai_reply)
            logging.info(f"[{worker_id}] 任務完成，結果已寫入資料庫。")

            self.task_queue.task_done()

    def save_record(self, timestamp, prompt, response):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO api_logs (timestamp, prompt, response) VALUES (?, ?, ?)",
            (timestamp, prompt, response)
        )
        conn.commit()
        conn.close()

    def shutdown(self):
        self.is_running = False

if __name__ == "__main__":
    # 使用你提供的 Groq API 金鑰
    MY_GROQ_KEY = "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"

    engine = WorldClassEngineWithAPI(MY_GROQ_KEY)

    # 啟動背景 Worker
    t = threading.Thread(target=engine.worker_node, args=("API-Worker-01",))
    t.daemon = True
    t.start()

    # 提交真實的 AI 查詢任務
    engine.submit_prompt("請用一句話介紹 Python 在分散式系統中的優勢。")

    time.sleep(5.0)
    engine.shutdown()
    logging.info("真實 API 系統演練圓滿結束！")
import queue
import threading
import time
import datetime
import sqlite3
import logging
import requests
import json

# 設定系統日誌格式
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] ⚡ [真實 API 大腦]: %(message)s"
)

class RealAPIBrain:
    """串接真實世界 AI API 的大腦模組"""
    def __init__(self, api_key):
        self.api_key = api_key
        self.api_url = "https://api.groq.com/openai/v1/chat/completions"

    def query_llm(self, prompt):
        logging.info(f"🧠 [Groq 大腦] 正在透過真實 API 發送推理請求...")

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "llama-3.3-70b-versatile",
            "messages": [
                {"role": "system", "content": "你是一個世界級的程式開發與 AI 系統夥伴。"},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7
        }

        try:
            response = requests.post(self.api_url, headers=headers, json=payload, timeout=10)
            if response.status_code == 200:
                result_json = response.json()
                answer = result_json['choices'][0]['message']['content']
                return f"API 推理成功: {answer.strip()}"
            else:
                return f"API 錯誤代碼 {response.status_code}: {response.text}"
        except Exception as e:
            return f"連線例外狀況: {e}"

class WorldClassEngineWithAPI:
    """結合世界級訊息佇列與真實 API 大腦的總成系統"""
    def __init__(self, api_key, db_name="real_api_system.db"):
        self.db_name = db_name
        self.init_database()
        self.task_queue = queue.Queue()
        self.is_running = True

        # 初始化真實 API 大腦
        self.brain = RealAPIBrain(api_key)
        logging.info("真實 API 總成引擎初始化完成。")

    def init_database(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS api_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                prompt TEXT,
                response TEXT
            )
        ''')
        conn.commit()
        conn.close()

    def submit_prompt(self, prompt):
        self.task_queue.put(prompt)
        logging.info(f"⚡ 成功派發推理任務 -> {prompt}")

    def worker_node(self, worker_id):
        logging.info(f"⚙️ 工作節點 [{worker_id}] 已上線。")
        while self.is_running:
            try:
                prompt = self.task_queue.get(timeout=1.0)
            except queue.Empty:
                continue

            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logging.info(f"[{worker_id}] 正在處理提示詞: {prompt}")

            # 呼叫真實 API 取得 AI 回應
            ai_reply = self.brain.query_llm(prompt)

            # 寫入 SQLite 資料庫持久化
            self.save_record(timestamp, prompt, ai_reply)
            logging.info(f"[{worker_id}] 任務完成，結果已寫入資料庫。")

            self.task_queue.task_done()

    def save_record(self, timestamp, prompt, response):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO api_logs (timestamp, prompt, response) VALUES (?, ?, ?)",
            (timestamp, prompt, response)
        )
        conn.commit()
        conn.close()

    def shutdown(self):
        self.is_running = False

if __name__ == "__main__":
    # 使用你提供的 Groq API 金鑰
    MY_GROQ_KEY = "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"

    engine = WorldClassEngineWithAPI(MY_GROQ_KEY)

    # 啟動背景 Worker
    t = threading.Thread(target=engine.worker_node, args=("API-Worker-01",))
    t.daemon = True
    t.start()

    # 提交真實的 AI 查詢任務
    engine.submit_prompt("請用一句話介紹 Python 在分散式系統中的優勢。")

    time.sleep(5.0)
    engine.shutdown()
    logging.info("真實 API 系統演練圓滿結束！")

