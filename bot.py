import time
import datetime
import requests

# 設定兩組金鑰
GROQ_API_KEY = "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"
GEMINI_API_KEY = "AQ.Ab8RN6JOliVUP_vhxjatYWIraxRUtDqEy4mnWeS-CjEfii4ynA"

def generate_with_failover():
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"\n⏰ [{current_time}] 🚀 【雙引擎頂規產線啟動】...")
    
    prompt_text = (
        "You are an elite YouTube Shorts creator. "
        "Invent a totally unique, fascinating, and 100% safe fact. "
        "You MUST assign a category strictly chosen from: "
        "【歷史】, 【科學】, 【大自然】, 【奇聞】. "
        "Output in Traditional Chinese with: "
        "0. 影片分類 "
        "1. 解鎖趣味主題 "
        "2. 吸睛標題 "
        "3. 前3秒黃金口白 (禁『你知道嗎』) "
        "4. 30秒口白腳本 "
        "5. AI影片生片提示詞 (9:16 English, <40 words)"
    )
    
    result = None
    engine_used = ""
    
    # ==========================================
    # 1. 嘗試主引擎：Groq (最新 gpt-oss-120b)
    # ==========================================
    try:
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
        payload = {
            "model": "openai/gpt-oss-120b",
            "messages": [{"role": "user", "content": prompt_text}],
            "temperature": 1.0
        }
        res = requests.post(url, headers=headers, json=payload, timeout=35)
        if res.status_code == 200:
            result = res.json()['choices'][0]['message']['content'].strip()
            engine_used = "Groq (gpt-oss-120b)"
        else:
            print(f"⚠️ Groq 狀態碼異常 ({res.status_code})，切換至備援引擎...")
    except Exception as e:
        print(f"⚠️ Groq 連線例外 ({e})，切換至備援引擎...")

    # ==========================================
    # 2. 備援引擎：Gemini (最新 gemini-3.7-flash)
    # ==========================================
    if not result:
        print(f"🔄 【自動容錯】正在透過 Gemini 3.7 Flash 備援引擎產生內容...")
        try:
            gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.7-flash:generateContent?key={GEMINI_API_KEY}"
            headers = {"Content-Type": "application/json"}
            payload = {
                "contents": [{"parts": [{"text": prompt_text}]}]
            }
            res = requests.post(gemini_url, headers=headers, json=payload, timeout=40)
            if res.status_code == 200:
                data = res.json()
                result = data['candidates'][0]['content']['parts'][0]['text'].strip()
                engine_used = "Gemini (3.7-flash)"
            else:
                print(f"❌ Gemini 備援失敗 (狀態碼: {res.status_code}, 內容: {res.text})")
        except Exception as e:
            print(f"❌ Gemini 備援發生例外錯誤: {e}")

    # ==========================================
    # 3. 自動分類與儲存
    # ==========================================
    if result:
        print(f"✅ 成功透過 【{engine_used}】 產出文案！")
        print(result)
        print("-" * 50)
        
        category_file = "shorts_general.txt"
        if "歷史" in result: category_file = "history_shorts.txt"
        elif "科學" in result: category_file = "science_shorts.txt"
        elif "大自然" in result: category_file = "nature_shorts.txt"
        elif "奇聞" in result: category_file = "bizarre_shorts.txt"
            
        with open(category_file, "a", encoding="utf-8") as f:
            f.write(f"--- [{engine_used}] {current_time} ---\n" + result + "\n\n" + "="*40 + "\n\n")
            
        print(f"📁 【自動歸檔成功】已存入：{category_file}")
    else:
        print("❌ 雙引擎皆告失敗，本次循環跳過...")

# ==========================================
# 🚀 常駐主迴圈 (每 30 分鐘執行一次)
# ==========================================
INTERVAL_SECONDS = 1800  

print("♾️ 【雙引擎頂規機器人已就緒】...")

while True:
    try:
        generate_with_failover()
    except Exception as outer_e:
        print(f"🛡️ 系統防護攔截: {outer_e}，10秒後重啟...")
        time.sleep(10)
        
    print(f"💤 進入休眠，等待下一次定時...\n")
    time.sleep(INTERVAL_SECONDS)

