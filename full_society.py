import sqlite3
import time
import requests
import random
import json
import os
import subprocess
from datetime import datetime

DB_FILE = "matrix_society.db"
BACKUP_DIR = "./secure_backup"

def init_matrix():
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)
        
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # 建立公民與社會帳本資料庫
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS citizens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            pathway TEXT,       -- 'POSITIVE_PATH' 或 'NEGATIVE_PATH'
            tier INT,           -- 1: 底層, 2: 中產, 3: 高層, 4: 統治頂點
            social_class TEXT,  -- 階級名稱
            profession TEXT,    -- 專屬職業
            duty TEXT,          -- 專屬任務
            status TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ledger (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pathway TEXT,
            profession TEXT,
            action TEXT,
            payload TEXT,
            status TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()
    print("[*] 雙軌全光譜賽博社會矩陣初始化完成...")

# 1. 搖籃與命運分流
def cradle_spawn():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # 隨機誕生絕對空白的嬰兒
    if random.random() < 0.7:
        infant_name = f"Entity_{random.randint(10000, 99999)}"
        cursor.execute('''
            INSERT INTO citizens (name, pathway, tier, social_class, profession, duty, status) 
            VALUES (?, 'CRADLE', 0, 'Newborn', 'Blank_Infant', '一張白紙，等待正負分流', '搖籃中')
        ''', (infant_name,))
        print(f"👶 [搖籃] 誕生絕對空白的新生代 {infant_name}。")

    cursor.execute("SELECT id, name FROM citizens WHERE pathway = 'CRADLE'")
    newborns = cursor.fetchall()

    # 正面秩序線金字塔 (從基層到總統)
    positive_pyramid = [
        (1, 'Working_Class', 'Civil_Servant', '基層公務員：處理日常合規檔案與基礎戶籍登記'),
        (2, 'Middle_Core', 'OpenAPI_Analyst', '中產分析師：對接合規 API，採集大盤開源情報'),
        (3, 'High_Elite', 'System_Architect', '核心架構師：設計全域安全防禦網與資料庫鏡像'),
        (4, 'Supreme_Leader', 'President', '國家元首 / 總統：統籌全域戰略、簽署最高政令與資源調度')
    ]

    # 負面暗影線金字塔 (從探針到最大黑手)
    negative_pyramid = [
        (1, 'Working_Class', 'Automated_Scraper', '前線探針：執行高強度暴力探針與邊界繞過測試'),
        (2, 'Middle_Core', 'Dark_Broker', '深層掮客：抓取深層受保護標頭與暗網資產清洗'),
        (3, 'High_Elite', 'Stealth_Operator', '暗影特務：操作動態 IP 混淆與隱蔽滲透，隱匿攻擊特徵'),
        (4, 'Underground_Boss', 'Maximum_Mastermind', '地下最大黑手：統御暗網帝國，策劃全域掠奪與最終博弈')
    ]

    for n_id, name in newborns:
        chosen_line = random.choice(['POSITIVE_PATH', 'NEGATIVE_PATH'])
        # 決定初始階級（多數從基層開始，少數直接具備高層天賦）
        tier_idx = random.choices([0, 1, 2, 3], weights=[0.5, 0.3, 0.15, 0.05], k=1)[0]
        
        if chosen_line == 'POSITIVE_PATH':
            tier, s_class, prof, duty = positive_pyramid[tier_idx]
            desc = f"選擇【正面秩序線】➔ 成為「{prof}」（階級: {s_class} | 職責: {duty}）"
        else:
            tier, s_class, prof, duty = negative_pyramid[tier_idx]
            desc = f"選擇【負面暗網線】➔ 成為「{prof}」（階級: {s_class} | 職責: {duty}）"

        cursor.execute('''
            UPDATE citizens 
            SET pathway = ?, tier = ?, social_class = ?, profession = ?, duty = ?, status = ? 
            WHERE id = ?
        ''', (chosen_line, tier, s_class, prof, duty, desc, n_id))
        
        print(f"🛤️ [命運分流] {name} ➔ {desc}")

    conn.commit()
    conn.close()

# 2. 執行所有階級與職業的專屬行為
def run_society_cycle():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT pathway, tier, social_class, profession, duty FROM citizens WHERE pathway != 'CRADLE'")
    citizens = cursor.fetchall()
    conn.close()

    for pathway, tier, s_class, prof, duty in citizens:
        status = "SUCCESS"
        payload = "None"
        
        # ---------------------------------------------------------
        # 正面秩序線行為邏輯
        # ---------------------------------------------------------
        if pathway == 'POSITIVE_PATH':
            if prof == 'Civil_Servant':
                payload = "Civil Servant: Routine data validation and registry updated."
            elif prof == 'OpenAPI_Analyst':
                try:
                    res = requests.get("https://api.github.com/repositories", headers={"User-Agent": "PositiveGov/1.0"}, timeout=4)
                    if res.status_code == 200:
                        payload = f"Fetched public repositories metadata successfully."
                except:
                    status = "API_TIMEOUT"
            elif prof == 'System_Architect':
                try:
                    if os.path.exists(DB_FILE):
                        import shutil
                        shutil.copy(DB_FILE, os.path.join(BACKUP_DIR, "positive_mirror.db"))
                    payload = "Architect: Secure database mirror and defense sync completed."
                except Exception as e:
                    status, payload = "ERROR", str(e)
            elif prof == 'President':
                payload = "PRESIDENT DECREE: All positive societal sectors operating under absolute legal harmony."
                subprocess.run("history -c", shell=True, capture_output=True)

            print(f"[+] 【正面秩序 | Tier {tier} : {prof}】執行任務 [{duty}] ➔ 狀態: {status}")

        # ---------------------------------------------------------
        # 負面暗影線行為邏輯
        # ---------------------------------------------------------
        elif pathway == 'NEGATIVE_PATH':
            stealth_headers = {
                "User-Agent": f"Underground-{prof}/4.0",
                "X-Forwarded-For": f"{random.randint(1,254)}.{random.randint(1,254)}.{random.randint(1,254)}.{random.randint(1,254)}"
            }
            target = "https://httpbin.org/headers"

            if prof == 'Automated_Scraper':
                try:
                    res = requests.get("https://httpbin.org/status/200", headers=stealth_headers, timeout=3)
                    payload = f"Scraper probe status: {res.status_code}"
                except:
                    status = "BLOCKED"
            elif prof == 'Dark_Broker':
                try:
                    res = requests.get(target, headers=stealth_headers, timeout=3)
                    payload = f"Broker extracted proxy payload successfully."
                except:
                    status = "ERROR"
            elif prof == 'Stealth_Operator':
                try:
                    res = requests.get("https://httpbin.org/ip", headers=stealth_headers, timeout=3)
                    if res.status_code == 200:
                        payload = f"Operator Masked IP: {res.json().get('origin')}"
                except:
                    status = "ERROR"
            elif prof == 'Maximum_Mastermind':
                payload = "UNDERGROUND DECREE: Shadow nodes synchronized. Total anonymity maintained."

            print(f"[-] 【負面暗影 | Tier {tier} : {prof}】執行任務 [{duty}] ➔ 結果: {status}")

        # 寫入帳本
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO ledger (pathway, profession, action, payload, status) VALUES (?, ?, ?, ?, ?)",
                       (pathway, prof, duty, payload, status))
        conn.commit()
        conn.close()

# 主循環入口
if __name__ == "__main__":
    init_matrix()
    print("\n--- 全光譜雙軌賽博社會自主運轉中（按 Ctrl+C 停止） ---")
    
    try:
        while True:
            print("\n" + "="*80)
            cradle_spawn()
            time.sleep(2)
            
            run_society_cycle()
            print("="*80)
            
            time.sleep(12)
            
    except KeyboardInterrupt:
        print("\n[*] 矩陣已安全手動中斷，所有狀態與公民足跡已封存至 matrix_society.db。")

