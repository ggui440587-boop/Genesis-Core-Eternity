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


# --- 1. 安全限流版 GitHub 爬蟲 ---
def crawl_github(cursor, conn):
    print("🐙 [安全模式] 正在請求 GitHub API...")
    url = "https://api.github.com/search/repositories?q=language:python&sort=stars&order=desc&per_page=10"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "User-Agent": "SafeResearchBot/1.0"
    }
    
    try:
        response = requests.get(url, headers=headers)
        
        # 檢查是否觸發 GitHub 流量限制 (Rate Limit)
        if response.status_code == 429 or 'X-RateLimit-Remaining' in response.headers and int(response.headers['X-RateLimit-Remaining']) == 0:
            print("⚠️ 警告：觸發 GitHub 流量限制，強制暫停 60 秒...")
            time.sleep(60)
            return

        if response.status_code == 200:
            items = response.json().get("items", [])
            for item in items:
                cursor.execute(
                    "INSERT OR IGNORE INTO repos (id, name, description, category, source) VALUES (?, ?, ?, ?, ?)",
                    (f"gh_{item['id']}", item['full_name'], item.get('description') or '無描述', '未分類', 'GitHub')
                )
            conn.commit()
            print(f"✅ GitHub 成功抓取並寫入 {len(items)} 筆資料。")
        else:
            print(f"❌ GitHub 抓取失敗，狀態碼：{response.status_code}")
            
    except Exception as e:
        print(f"❌ GitHub 發生例外錯誤: {e}")
    
    # 禮貌性暫停 3 秒，保護 API 頻率
    time.sleep(3)


# --- 2. 安全限流版 Hugging Face 爬蟲 ---
def crawl_huggingface(cursor, conn):
    print("🤗 [安全模式] 正在請求 Hugging Face API...")
    url = "https://huggingface.co/api/models?sort=downloads&direction=-1&limit=10"
    headers = {
        "Authorization": f"Bearer {HF_TOKEN}"
    }
    
    try:
        response = requests.get(url, headers=headers)
        
        if response.status_code == 429:
            print("⚠️ 警告：觸發 Hugging Face 流量限制，強制暫停 60 秒...")
            time.sleep(60)
            return

        if response.status_code == 200:
            models = response.json()
            count = 0
            for m in models:
                downloads = m.get("downloads", 0)
                likes = m.get("likes", 0)
                desc = f"下載次數: {downloads:,}, 愛心數: {likes}"
                cursor.execute(
                    "INSERT OR IGNORE INTO repos (id, name, description, category, source) VALUES (?, ?, ?, ?, ?)",
                    (f"hf_{m['id']}", m['id'], desc, '未分類', 'Hugging Face')
                )
                count += 1
            conn.commit()
            print(f"✅ Hugging Face 成功抓取並寫入 {count} 筆資料。")
        else:
            print(f"❌ Hugging Face 抓取失敗，狀態碼：{response.status_code}")
            
    except Exception as e:
        print(f"❌ Hugging Face 發生例外錯誤: {e}")
    
    # 禮貌性暫停 3 秒
    time.sleep(3)


# --- 3. 批次 AI 智慧分類（自動消化未分類） ---
def ai_process():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # 迴圈自動處理，直到所有「未分類」被清空為止
    while True:
        cursor.execute("SELECT id, name, description FROM repos WHERE category = '未分類' LIMIT 10")
        batch = cursor.fetchall()
        
        if not batch:
            print("💡 目前沒有需要 AI 分類的新資料，收工！")
            break

        print(f"🤖 Groq AI 正在批次分類（剩餘待分類: {len(batch)} 筆）...")
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
            
            # 如果 Groq 告知流量過載 (429)，自動暫停 10 秒後重試
            if response.status_code == 429:
                print("⚠️ AI 請求過快（觸發流量限制），冷卻 10 秒後繼續...")
                time.sleep(10)
                continue
                
            res_data = response.json()
            if "choices" not in res_data:
                print(f"⚠️ AI 回傳格式異常: {res_data}")
                break
                
            content = res_data['choices'][0]['message']['content']
            results = json.loads(content).get("results", [])
            
            for item in results:
                cursor.execute("UPDATE repos SET category = ? WHERE id = ?", (item['category'], item['id']))
            conn.commit()
            print("✅ 這一批 AI 分類成功！")
            
        except Exception as e:
            print(f"❌ AI 處理發生錯誤: {e}")
            break
        
        # 每次 AI 請求之間暫停 2 秒，保護 Groq 額度
        time.sleep(2)
    
    conn.close()

if __name__ == "__main__":
    database = init_db()
    cursor = database.cursor()
    
    # 執行有限制的安全爬蟲
    crawl_github(cursor, database)
    crawl_huggingface(cursor, database)
    database.close()
    
    # 自動把所有未分類一次清空
    ai_process()
    print("🎉 本次自動排程圓滿結束！")

