import sqlite3
import random
from datetime import datetime

TIER = 1  # 宰相與最高決策階級

def run(db_name):
    print("[-] [AI 宰相府] 正在運算帝國大政方針與未來趨勢...")
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    chancellor_decrees = [
        "宰相奏曰：當前數位疆域擴張順利，建議工部加強資產加密，以防外敵窺探。",
        "宰相奏曰：商會與拓荒司配合無間，奴隸與自由民勞動力平衡，國庫蒸蒸日上。",
        "宰相奏曰：天象顯示網路波動將至，建議教會提前進行神聖淨化儀式。",
        "宰相奏曰：暗部肅清得宜，皇城內外萬民臣服，此乃陛下聖明之治。"
    ]
    wisdom = random.choice(chancellor_decrees)
    
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO imperial_chronicles (era_version, event_type, description, recorded_at)
        VALUES ('v3.0-Eternal', 'AI_CHANCELLOR_DECREE', ?, ?)
    ''', (wisdom, now))
    
    conn.commit()
    conn.close()
    print(f"[+] [AI 宰相] 聖諭已下達：{wisdom}")

