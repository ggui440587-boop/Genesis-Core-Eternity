import os
import requests
import sqlite3
from datetime import datetime

# 1. 抓取 GitHub Trending 當日熱門專案
def fetch_github_trending():
    url = "https://api.github.com/search/repositories?q=language:python+sort:stars&order=desc"
    headers = {"Accept": "application/vnd.github.v3+json"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        items = response.json().get("items", [])
        if items:
            repo = items[0]
            return {
                "name": repo["name"],
                "description": repo["description"] or "無專案描述",
                "url": repo["html_url"],
                "stars": repo["stargazers_count"]
            }
    return None

# 2. 生成短影音腳本
def generate_video_script(repo):
    if not repo:
        return "今天沒有抓到專案資料"
    
    script = f"""
【短影音 30 秒腳本：GitHub 專案自動追蹤】

[0-3秒 痛點吸睛]
「還在手動盲目刷 GitHub 找好用工具？教你一招，每天自動把全網最猛的開源專案抓出來！」

[3-20秒 核心乾貨]
「今天全網最火紅的開源專案叫 {repo['name']}！
它主要是：{repo['description']}
目前已經累積了 {repo['stars']} 個星星。
只要用 Python 寫個簡單的 API 腳本，結合自動化排程，每天定時把這種爆款專案清單直接推送到你的手機，讓你永遠走在技術最前線！」

[20-30秒 導流變現]
「想要這個自動化爬蟲的完整原始碼和工作流程模板嗎？點擊我主頁連結，馬上解鎖你的自動化工具包！」
"""
    return script

# 3. 儲存到本機 SQLite 資料庫 (fusion_hub.db)
def save_to_db(repo, script):
    db_path = "fusion_hub.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS video_scripts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            repo_name TEXT,
            script TEXT
        )
    """)
    cursor.execute("INSERT INTO video_scripts (date, repo_name, script) VALUES (?, ?, ?)",
                   (datetime.now().strftime("%Y-%m-%d"), repo["name"], script))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    print("正在從 GitHub 抓取今日熱門專案...")
    repo_data = fetch_github_trending()
    if repo_data:
        print(f"成功抓取專案: {repo_data['name']}")
        video_script = generate_video_script(repo_data)
        save_to_db(repo_data, video_script)
        print("\n--- 生成的腳本內容 ---")
        print(video_script)
        print("\n已成功存入本機資料庫 (fusion_hub.db)！")
    else:
        print("抓取失敗，請檢查網路連線。")

