import queue
import threading
import time
import datetime
import sqlite3
import logging
import requests

# 設定系統日誌格式
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] 🟢 [免費額度保護引擎]: %(message)s"
)

class FreeTierAPIBrain:
    """嚴格遵守免費額度的真實 API 大腦模組"""
    def __init__(self, api_key):
        self.api_key = api_key
        self.api_url = "https://api.groq.com/openai/v1/chat/completions"

    def query_llm_free_tier(self, prompt):
        logging.info(f"🧠 [免費用戶通道] 正在發送請求至 Groq API...")

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "llama-3.3-70b-versatile",
            "messages": [
                {"role": "system", "content": "你是一個精準且高效的程式開發夥伴。"},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.5
        }

        try:
            response = requests.post(self.api_url, headers=headers, json=payload, timeout=10)

            if response.status_code == 200:
                result_json = response.json()
                answer = result_json['choices'][0]['message']['content']
                return f"免費推理成功: {answer.strip()}"
            elif response.status_code == 429:
                logging.warning("⚠️ 觸發速率限制（Rate Limit），免費額度冷卻中...")
                return "免費額度保護：請求過快，已觸發速率限制保護。"
            else:
                return f"API 狀態碼 {response.status_code}: {response.text}"

        except Exception as e:
            return f"連線例外狀況: {e}"

class FreeTierSafeEngine:
    """結合免費額度保護與佇列的總成系統"""
    def __init__(self, api_key, db_name="free_tier_system.db"):
        self.db_name = db_name
        self.init_database()
        self.task_queue = queue.Queue()
        self.is_running = True
        self.brain = FreeTierAPIBrain(api_key)
        logging.info("免費額度防護引擎初始化完成。")

    def init_database(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS free_logs (
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
        logging.info(f"⚡ 安全排入免費佇列 -> {prompt}")

    def worker_node(self, worker_id):
        logging.info(f"⚙️ 節點 [{worker_id}] 已上線，隨時準備安全處理任務。")
        while self.is_running:
            try:
                prompt = self.task_queue.get(timeout=1.0)
            except queue.Empty:
                continue

            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # 呼叫免費額度大腦
            ai_reply = self.brain.query_llm_free_tier(prompt)

            # 寫入資料庫
            try:
                conn = sqlite3.connect(self.db_name)
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO free_logs (timestamp, prompt, response) VALUES (?, ?, ?)",
                    (timestamp, prompt, ai_reply)
                )
                conn.commit()
                conn.close()
            except Exception as db_err:
                logging.error(f"資料庫寫入錯誤: {db_err}")

            logging.info(f"[{worker_id}] 任務安全完成。")
            self.task_queue.task_done()

            # 關鍵：免費額度冷卻時間（確保每筆請求之間間隔 3 秒，絕不超速）
            logging.info("⏳ 正在進行免費額度安全冷卻（等待 3 秒）...")
            time.sleep(3.0)

    def shutdown(self):
        self.is_running = False

if __name__ == "__main__":
    # 使用你提供的 Groq API 金鑰
    MY_GROQ_KEY = "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"

    engine = FreeTierSafeEngine(MY_GROQ_KEY)

    t = threading.Thread(target=engine.worker_node, args=("Free-Worker-01",))
    t.daemon = True
    t.start()

    # 提交測試任務
    engine.submit_prompt("請用繁體中文列出 Python 的三個核心特點。")

    # 等待任務執行與冷卻
    time.sleep(6.0)
    engine.shutdown()
    logging.info("免費額度系統演練圓滿結束！")

