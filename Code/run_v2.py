import requests
import sqlite3
import time
import json

# --- 整合你的所有金鑰與設定 ---
DB_NAME = 'fusion_hub.db'

# 選擇 Groq 作為 AI 分類主力
AI_API_URL = "https://api.groq.com/openai/v1/chat/completions"
AI_API_KEY = "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"
AI_MODEL = "llama-3.3-70b-versatile"

# GitHub 專用 Token
GITHUB_TOKEN = "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"

# Hugging Face Token
HF_TOKEN = "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"


# --- 1. 資料庫初始化 ---
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

# --- 2A. 抓取 GitHub 專案 ---
def crawl_github(cursor, conn):
    print("🐙 正在安全抓取 GitHub 熱門專案...")
    url = "https://api.github.com/search/repositories?q=language:python&sort=stars&order=desc&per_page=10"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "User-Agent": "FusionBot/1.0"
    }
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            items = response.json().get("items", [])
            for item in items:
                cursor.execute(
                    "INSERT OR IGNORE INTO repos (id, name, description, category, source) VALUES (?, ?, ?, ?, ?)",
                    (f"gh_{item['id']}", item['full_name'], item.get('description') or '無描述', '未分類', 'GitHub')
                )
            conn.commit()
            print("✅ GitHub 專案抓取並去重完畢！")
        else:
            print(f"❌ GitHub 抓取失敗，狀態碼：{response.status_code}")
    except Exception as e:
        print(f"❌ GitHub 發生錯誤: {e}")

# --- 2B. 抓取 Hugging Face 模型 ---
def crawl_huggingface(cursor, conn):
    print("🤗 正在抓取 Hugging Face AI 模型...")
    url = "https://huggingface.co/api/models?sort=downloads&direction=-1&limit=10"
    headers = {
        "Authorization": f"Bearer {HF_TOKEN}"
    }
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            models = response.json()
            for m in models:
                downloads = m.get("downloads", 0)
                likes = m.get("likes", 0)
                desc = f"下載次數: {downloads:,}, 愛心數: {likes}"
                cursor.execute(
                    "INSERT OR IGNORE INTO repos (id, name, description, category, source) VALUES (?, ?, ?, ?, ?)",
                    (f"hf_{m['id']}", m['id'], desc, '未分類', 'Hugging Face')
                )
            conn.commit()
            print("✅ Hugging Face 模型抓取並去重完畢！")
        else:
            print(f"❌ Hugging Face 抓取失敗，狀態碼：{response.status_code}")
    except Exception as e:
        print(f"❌ Hugging Face 發生錯誤: {e}")

# --- 3. 透過 Groq AI 進行極速智慧分類 (含錯誤診斷) ---
def ai_process():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, name, description FROM repos WHERE category = '未分類' LIMIT 15")
    batch = cursor.fetchall()
    
    if not batch:
        print("💡 目前沒有需要 AI 分類的新資料。")
        conn.close()
        return

    print(f"🤖 Groq AI 開始進行智慧分類（共 {len(batch)} 筆）...")
    data_to_send = [{"id": r[0], "name": r[1], "desc": r[2]} for r in batch]
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {AI_API_KEY}"
    }
    
    prompt = f"""
    請將以下開源專案與模型歸類為這幾類之一：[網頁開發, 人工智慧, 資料科學, 工具腳本, 其他]。
    必須以嚴格的 JSON 格式回傳，結構必須包含一個 "results" 陣列，例如:
    {{"results": [{{"id": "專案id", "category": "分類名稱"}}, ...]}}
    
    資料清單：
    {json.dumps(data_to_send, ensure_ascii=False)}
    """
    
    payload = {
        "model": AI_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "response_format": {"type": "json_object"}
    }
    
    try:
        response = requests.post(AI_API_URL, headers=headers, json=payload)
        res_data = response.json()
        
        # 診斷檢查：如果回傳結構不對，印出來看
        if "choices" not in res_data:
            print(f"⚠️ Groq 回傳了未預期的內容: {res_data}")
            return
            
        content = res_data['choices'][0]['message']['content']
        results = json.loads(content).get("results", [])
        
        for item in results:
            cursor.execute("UPDATE repos SET category = ? WHERE id = ?", (item['category'], item['id']))
        conn.commit()
        print("✅ AI 智慧分類完成並更新資料庫！")
    except Exception as e:
        print(f"❌ AI 處理錯誤: {e}")
    
    conn.close()

if __name__ == "__main__":
    database = init_db()
    cursor = database.cursor()
    
    # 1. 執行雙源爬蟲
    crawl_github(cursor, database)
    time.sleep(1)
    crawl_huggingface(cursor, database)
    database.close()
    
    # 2. 執行 AI 分類
    ai_process()
    print("🎉 全流程執行完畢！資料已安全儲存於 fusion_hub.db")

