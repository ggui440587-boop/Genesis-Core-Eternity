import requests
import sqlite3
import time
import json

# --- 系統設定 ---
DB_NAME = 'fusion_hub.db'
AI_API_URL = "https://api.groq.com/openai/v1/chat/completions"
AI_API_KEY = "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"
AI_MODEL = "openai/gpt-oss-20b"
GITHUB_TOKEN = "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"
HF_TOKEN = "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"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS repos (
            id TEXT PRIMARY KEY,
            name TEXT,
            description TEXT,
            category TEXT DEFAULT '未分類',
            source TEXT
        )
    ''')
    conn.commit()
    return conn

def run_task():
    print(f"\n⏰ [自動排程啟動] 時間: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    conn = init_db()
    cursor = conn.cursor()
    
    # 1. 抓 GitHub
    try:
        res = requests.get("https://api.github.com/search/repositories?q=language:python&sort=stars&order=desc&per_page=5", 
                           headers={"Authorization": f"token {GITHUB_TOKEN}", "User-Agent": "Bot/1.0"})
        if res.status_code == 200:
            for item in res.json().get("items", []):
                cursor.execute("INSERT OR IGNORE INTO repos (id, name, description, category, source) VALUES (?, ?, ?, ?, ?)",
                               (f"gh_{item['id']}", item['full_name'], item.get('description') or '無描述', '未分類', 'GitHub'))
            conn.commit()
            print("✅ GitHub 抓取完成")
    except Exception as e:
        print(f"❌ GitHub 錯誤: {e}")
    
    time.sleep(2)
    
    # 2. 抓 Hugging Face
    try:
        res = requests.get("https://huggingface.co/api/models?sort=downloads&direction=-1&limit=5",
                           headers={"Authorization": f"Bearer {HF_TOKEN}"})
        if res.status_code == 200:
            for m in res.json():
                desc = f"下載次數: {m.get('downloads', 0):,}"
                cursor.execute("INSERT OR IGNORE INTO repos (id, name, description, category, source) VALUES (?, ?, ?, ?, ?)",
                               (f"hf_{m['id']}", m['id'], desc, '未分類', 'Hugging Face'))
            conn.commit()
            print("✅ Hugging Face 抓取完成")
    except Exception as e:
        print(f"❌ HF 錯誤: {e}")
        
    conn.close()
    
    # 3. AI 分類
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    while True:
        cursor.execute("SELECT id, name, description FROM repos WHERE category = '未分類' LIMIT 10")
        batch = cursor.fetchall()
        if not batch:
            break
        
        data_to_send = [{"id": r[0], "name": r[1], "desc": r[2]} for r in batch]
        try:
            response = requests.post(AI_API_URL, 
                                     headers={"Content-Type": "application/json", "Authorization": f"Bearer {AI_API_KEY}"},
                                     json={
                                         "model": AI_MODEL,
                                         "messages": [{"role": "user", "content": f"將以下專案歸類為[網頁開發, 人工智慧, 資料科學, 工具腳本, 其他]，以嚴格JSON回傳 {{\"results\": [{{\"id\":\"...\",\"category\":\"...\"}}]}}: {json.dumps(data_to_send, ensure_ascii=False)}"}],
                                         "response_format": {"type": "json_object"}
                                     })
            res_data = response.json()
            if "choices" in res_data:
                content = res_data['choices'][0]['message']['content']
                for item in json.loads(content).get("results", []):
                    cursor.execute("UPDATE repos SET category = ? WHERE id = ?", (item['category'], item['id']))
                conn.commit()
                print("🤖 這一批 AI 分類已更新")
        except Exception as e:
            print(f"❌ AI 錯誤: {e}")
            break
        time.sleep(2)
    conn.close()
    print("🎉 本次循環結束，進入休息狀態...")

if __name__ == "__main__":
    print("🚀 啟動自動循環爬蟲守護程式 (按 Ctrl+C 可隨時停止)")
    while True:
        run_task()
        time.sleep(3600)  # 每 1 小時執行一次

