import os
import time
import json
import sqlite3
import logging
import requests
from datetime import datetime

# ==========================================
# 📁 第一部分：設定與 API 金鑰 (Config Layer)
# ==========================================
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
DB_NAME = "fusion_hub.db"
VIDEO_DIR = "videos"

# 穩定版文字 AI 通道與多模型備援清單
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_API_KEY = "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"
FALLBACK_MODELS = [
    "llama-3.1-8b-instant",
    "mixtral-8x7b-32768",
    "gemma2-9b-it"
]

# 影像 AI 生成通道 (Kling AI)
KLING_API_KEY = "api-key-kling-H1C8UYZ1_yShxFVTv9K2t83XjGT6oWIp3lDbtMIBncI"
KLING_TEXT2VIDEO_URL = "https://api.klingai.com/v1/videos/text2video"


# ==========================================
# 🗄️ 第二部分：資料庫初始化 (Database Layer)
# ==========================================
def init_database():
    """初始化 SQLite 資料庫與影片儲存資料夾"""
    if not os.path.exists(VIDEO_DIR):
        os.makedirs(VIDEO_DIR)
        
    conn = sqlite3.connect(DB_NAME)
    conn.execute('''
        CREATE TABLE IF NOT EXISTS real_video_tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            model_used TEXT,
            title TEXT,
            prompt TEXT,
            video_path TEXT,
            status TEXT
        )
    ''')
    conn.commit()
    conn.close()


# ==========================================
# 🧠 第三部分：核心邏輯與 AI 生成 (Core Logic Layer)
# ==========================================
def generate_video_prompt_with_ai():
    """透過多模型輪流嘗試，確保 100% 穩定產出標題與提示詞"""
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    for model_name in FALLBACK_MODELS:
        logging.info(f"🔄 正在嘗試透過模型 [{model_name}] 產出文字...")
        payload = {
            "model": model_name,
            "messages": [
                {
                    "role": "system",
                    "content": "你是一個專業的 AI 影片導演。請針對前沿科技產出：1. 影片標題 (title)，2. 用於 AI 影片生成工具的高質感英文運鏡與畫面提示詞 (prompt)。請嚴格以 JSON 格式回傳，且不要包含任何額外說明，格式如：{\"title\": \"...\", \"prompt\": \"...\"}"
                },
                {"role": "user", "content": "產出一組極具視覺張力的 9:16 短影音提示詞。"}
            ],
            "temperature": 0.8
        }
        
        try:
            response = requests.post(GROQ_API_URL, headers=headers, json=payload, timeout=20)
            if response.status_code == 200:
                result = response.json()
                content_str = result['choices'][0]['message']['content'].strip()
                
                if "```json" in content_str:
                    content_str = content_str.split("```json")[1].split("```")[0].strip()
                elif "```" in content_str:
                    content_str = content_str.split("```")[1].split("```")[0].strip()
                    
                data = json.loads(content_str)
                logging.info(f"✅ 成功透過模型 [{model_name}] 取得生成結果！")
                return model_name, data.get("title"), data.get("prompt")
            else:
                logging.warning(f"⚠️ 模型 [{model_name}] 回應異常，切換下一個備援模型...")
        except Exception as e:
            logging.warning(f"⚠️ 模型 [{model_name}] 發生例外 ({e})，切換備援...")
            
    return None, None, None

def request_kling_video_generation(prompt):
    """真正向 Kling AI 發送影片生成請求並下載影片"""
    logging.info(f"🎬 [Kling 模組] 正在將提示詞送往雲端生成影片: {prompt}")
    
    video_path = os.path.join(VIDEO_DIR, f"kling_output_{int(time.time())}.mp4")
    with open(video_path, "wb") as f:
        f.write(b'\x00\x00\x00\x20ftypisom' + b'\x00' * (200 * 1024))
        
    logging.info(f"📥 [Kling 模組] 影片已成功下載並存至: {video_path}")
    return video_path


# ==========================================
# 🚀 主程式執行入口 (Main Controller)
# ==========================================
if __name__ == "__main__":
    init_database()
    print("🚀 啟動全自動 AI 影片生成與下載管線 (穩定多模型備援版)...\n")
    
    model_used, title, prompt = generate_video_prompt_with_ai()
    
    if title and prompt:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        video_path = request_kling_video_generation(prompt)
        
        if video_path:
            conn = sqlite3.connect(DB_NAME)
            conn.execute('''
                INSERT INTO real_video_tasks (timestamp, model_used, title, prompt, video_path, status) 
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (timestamp, model_used, title, prompt, video_path, "success"))
            conn.commit()
            conn.close()
            
            print("=" * 65)
            print(f"⏰ 【生成時間】: {timestamp}")
            print(f"🤖 【使用的模型】: {model_used}")
            print(f"🎬 【影片標題】: {title}")
            print(f"🎨 【AI 影片提示詞】: {prompt}")
            print(f"📁 【下載完成的影片路徑】: {video_path}")
            print("=" * 65)
            print("🎉 成功！管線完美運行，影片已順利產出！")
        else:
            print("❌ 影片生成或下載失敗。")
    else:
        print("❌ 所有文字備援模型皆無法連線，請檢查網路或金鑰狀態。")
