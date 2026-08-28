import sqlite3
import os
from datetime import datetime

TIER = 2  # 工部與技術階級

def run(db_name):
    print("[-] [工部] 正在盤點帝國基礎建設並執行 Git 遠端備份同步...")
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # 執行 Git 自動同步（前提是該目錄已初始化 Git 並設定好 remote）
    git_status = "SUCCESS"
    try:
        os.system("git add fusion_hub.db plugins/ > /dev/null 2>&1")
        os.system(f'git commit -m "Empire Auto-Backup: {now}" > /dev/null 2>&1')
        os.system("git push origin main > /dev/null 2>&1")
    except Exception:
        git_status = "LOCAL_ONLY"

    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO imperial_treasury (asset_name, quantity, last_updated)
        VALUES ('Ministry_Works_Score', 10, ?)
        ON CONFLICT(asset_name) 
        DO UPDATE SET quantity = quantity + 10, last_updated = excluded.last_updated
    ''', (now,))
    conn.commit()
    conn.close()
    print(f"[+] [工部] 建設完畢：資產與數據已透過 Git 封存 (狀態: {git_status})。")

