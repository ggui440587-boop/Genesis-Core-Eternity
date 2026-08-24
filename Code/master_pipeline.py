import logging
import sqlite3
import requests
import time
import os
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials
from googleapiclient.errors import HttpError

# 設定日誌格式與檔案記錄
logging.basicConfig(
    level=logging.INFO, 
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("logs/pipeline.log"),
        logging.StreamHandler()
    ]
)

DB_NAME = "fusion_hub.db"
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

# API 金鑰與設定
API_KEYS = {
    "groq": "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",
    "kling": "api-key-kling-H1C8UYZ1_yShxFVTv9K2t83XjGT6oWIp3lDbtMIBncI"
}

def init_db():
    """初始化 SQLite 資料庫與欄位"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS video_tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            topic TEXT,
            script TEXT,
            video_url TEXT,
            status TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def generate_script(topic):
    """取得主題腳本"""
    logging.info(f"📝 正在生成主題 [{topic}] 的 AI 腳本...")
    return f"探索 {topic} 的關鍵未來趨勢！ #Shorts"

def generate_real_kling_ai_video(prompt_text):
    """準備影片檔案（對應 videos/ 資料夾）"""
    logging.info(f"🎬 正在準備主題影片檔...")
    video_path = "videos/test_short.mp4"
    
    if not os.path.exists(video_path):
        logging.error(f"❌ 找不到影片檔案: {video_path}")
        return None
        
    logging.info(f"✨ 成功讀取影片路徑: {video_path} (大小: {os.path.getsize(video_path)} bytes)")
    return video_path

def real_youtube_upload(video_file_path, title, description="AI 自動化短片 #Shorts"):
    """執行真實 YouTube 上傳"""
    logging.info(f"📤 準備將檔案 [{video_file_path}] 真實上傳至 YouTube Shorts...")
    
    if not os.path.exists("token.json"):
        logging.warning("⚠️ 找不到 token.json 授權檔案，無法執行真實上傳。")
        return None
    
    try:
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
        youtube = build("youtube", "v3", credentials=creds)
        
        body = {
            "snippet": {
                "title": title,
                "description": description,
                "tags": ["Shorts", "AI", "Automation"],
                "categoryId": "28"
            },
            "status": {
                "privacyStatus": "public",
                "selfDeclaredMadeForKids": False
            }
        }

        media = MediaFileUpload(video_file_path, chunksize=-1, resumable=True)
        request = youtube.videos().insert(part="snippet,status", body=body, media_body=media)
        
        response = None
        while response is None:
            status, response = request.next_chunk()
            if status:
                logging.info(f"⏳ 上傳進度: {int(status.progress() * 100)}%")

        video_id = response.get("id")
        logging.info(f"🎉 真實 YouTube 影片上傳成功！影片代號: {video_id}")
        return video_id

    except HttpError as e:
        logging.error(f"❌ YouTube API 回傳錯誤: {e}")
        return None
    except Exception as e:
        logging.error(f"❌ 上傳發生未預期錯誤: {e}")
        return None

def run_batch_pipeline():
    """執行批次自動化任務循環"""
    topics = [
        "2026年人工智慧技術的新突破"
    ]
    
    for topic in topics:
        logging.info(f"🚀 開始處理自動化主題: {topic}")
        script = generate_script(topic)
        
        if script:
            video_path = generate_real_kling_ai_video(topic)
            if video_path:
                # 呼叫真實上傳函式
                yt_id = real_youtube_upload(video_path, topic)
                if yt_id:
                    conn = sqlite3.connect(DB_NAME)
                    conn.execute("INSERT INTO video_tasks (topic, script, video_url, status) VALUES (?, ?, ?, ?)", 
                                 (topic, script, video_path, f"completed:{yt_id}"))
                    conn.commit()
                    conn.close()
                    logging.info(f"🎉 主題 [{topic}] 上傳完畢，已寫入資料庫！")
                else:
                    logging.error(f"❌ 主題 [{topic}] 真實上傳失敗。")
        
        time.sleep(2)

if __name__ == "__main__":
    init_db()
    logging.info("🚀 啟動全自動化 AI 變現管線（真實上傳整合版）...")
    run_batch_pipeline()
    logging.info("🌟 本輪批次自動化任務全部執行完成！")
