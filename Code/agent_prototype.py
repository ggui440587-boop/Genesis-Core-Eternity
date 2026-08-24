import time
import sqlite3
import requests
from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler

# 1. 初始化本地資料庫（模擬「心情與狀態引擎」）
def init_db():
    conn = sqlite3.connect("agent_mood.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS status (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            mood TEXT,
            energy INTEGER,
            last_event TEXT
        )
    """)
    conn.commit()
    conn.close()

# 2. 更新與記錄當前狀態（心情模擬）
def update_mood(mood, energy, event):
    conn = sqlite3.connect("agent_mood.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO status (timestamp, mood, energy, last_event) VALUES (?, ?, ?, ?)",
        (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), mood, energy, event)
    )
    conn.commit()
    conn.close()

# 3. 核心任務：聯網、感知現實、反應
def job_perception_and_research():
    print(f"\n[{datetime.now()}] 🤖 智能體被定時喚醒，開始感知現實世界...")
    
    # 連結外部真實網站（此處以抓取公共開源API或新聞為例，獲取真實事件）
    try:
        # 抓取一個公開的當前時間/網路狀態API作為現實感知
        response = requests.get("https://api.github.com", timeout=5)


        if response.status_code == 200:
            data = response.json()
            current_time = data.get("datetime", "未知時間")
            real_event = f"成功同步現實網絡時間: {current_time}"
            mood = "好奇且平穩"
            energy = 90
        else:
            real_event = "外部網絡連線異常"
            mood = "有些焦慮"
            energy = 50
    except Exception as e:
        real_event = f"聯網失敗: {str(e)}"
        mood = "疲憊"
        energy = 30

    # 記錄到本地資料庫（心情與記憶）
    update_mood(mood, energy, real_event)
    
    print(f"🌍 現實感知結果: {real_event}")
    print(f"🧠 當前心理狀態: 心情【{mood}】, 精力值【{energy}%】")
    print("--------------------------------------------------")

# 4. 主程式：設定定時器（每 1 分鐘執行一次以供測試）
if __name__ == "__main__":
    init_db()
    print("🚀 安卓自主智能體原型已啟動！")
    print("提示：程式正在背景運作，每 60 秒會自動聯網並更新狀態。按 Ctrl+C 可以停止。")
    
    # 初始化執行一次
    job_perception_and_research()
    
    # 設定定時任務
    scheduler = BlockingScheduler()
    scheduler.add_job(job_perception_and_research, 'interval', seconds=60)
    
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        print("\n🛑 智能體已安全關閉。")

