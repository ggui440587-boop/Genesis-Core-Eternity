import os
import requests
import sqlite3
from datetime import datetime

DB_PATH = "fusion_hub.db"

# 初始化資料庫
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS video_scripts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            topic_type TEXT,
            script TEXT
        )
    """)
    conn.commit()
    conn.close()

# 主題一：抓取 GitHub 熱門專案 (技術/工具類)
def fetch_github_topic():
    url = "https://api.github.com/search/repositories?q=language:python+sort:stars&order=desc"
    headers = {"Accept": "application/vnd.github.v3+json"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        items = response.json().get("items", [])
        if items:
            repo = items[0]
            script = f"""
【30秒短影音腳本：GitHub 爆款開源工具】
[0-3秒 痛點吸睛]
「還在盲目搜尋好用的開源工具？教你一招，每天自動鎖定全網最猛的 Python 專案！」
[3-20秒 核心乾貨]
「今天全網討論度最高的是 {repo['name']}！
它主要是：{repo['description'] or '無描述'}
累積了高達 {repo['stargazers_count']} 個星星。
只要用自動化腳本串接，每天把這種頂級專案直接推送到你手上，永遠走在技術最前線！」
[20-30秒 導流變現]
「想要完整的自動化爬蟲原始碼和 n8n 模板嗎？點擊我主頁連結，馬上解鎖你的工具包！」
"""
            return "GitHub 熱門專案", script
    return None, None

# 主題二：抓取 Hacker News 熱門科技話題 (AI / 趨勢類)
def fetch_hackernews_topic():
    url = "https://hacker-news.firebaseio.com/v0/topstories.json"
    response = requests.get(url)
    if response.status_code == 200:
        story_ids = response.json()
        if story_ids:
            # 取第一筆熱門新聞 ID
            top_id = story_ids[0]
            story_url = f"https://hacker-news.firebaseio.com/v0/item/{top_id}.json"
            story_res = requests.get(story_url)
            if story_res.status_code == 200:
                story = story_res.json()
                title = story.get("title", "最新科技趨勢")
                script = f"""
【30秒短影音腳本：AI 與科技趨勢】
[0-3秒 痛點吸睛]
「別再錯過任何科技圈大事！教你用自動化腳本，每天第一時間掌握最震撼的產業內幕。」
[3-20秒 核心乾貨]
「今天 Hacker News 討論度爆表的話題是：{title}。
這代表業界正在往這個方向快速迭代！
不用自己辛苦刷論壇，讓自動化幫你過濾雜訊，每天只看最重要的乾貨。」
[20-30秒 導流變現]
「想要打造屬於你的自動化資訊過濾系統嗎？點擊主頁連結，領取完整設定教學與腳本！」
"""
                return "科技趨勢快報", script
    return None, None

# 儲存腳本到資料庫
def save_script(topic_type, script):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    today = datetime.now().strftime("%Y-%m-%d")
    cursor.execute("INSERT INTO video_scripts (date, topic_type, script) VALUES (?, ?, ?)",
                   (today, topic_type, script))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    # 根據日期奇偶數自動切換主題，實現內容不重複
    day_num = datetime.now().day
    if day_num % 2 == 0:
        print("正在執行：抓取 GitHub 技術主題...")
        t_type, script = fetch_github_topic()
    else:
        print("正在執行：抓取科技趨勢主題...")
        t_type, script = fetch_hackernews_topic()

    if script:
        save_script(t_type, script)
        print(f"\n[成功] 今日主題類型：{t_type}")
        print("--- 產出的腳本內容 ---")
        print(script)
        print("----------------------")
        print("已自動儲存至本機資料庫！")
    else:
        print("抓取失敗，請稍後再試。")

