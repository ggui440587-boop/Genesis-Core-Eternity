import sqlite3
from datetime import datetime

TIER = 3  # 商會與資產階級

def run(db_name):
    print("[-] [大商會] 正在穿梭邊境、收集數位資源與開源情報...")
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    # 累積帝國財政資產
    cursor.execute('''
        INSERT INTO imperial_treasury (asset_name, quantity, last_updated)
        VALUES ('Digital_Gold_Coins', 500, ?)
        ON CONFLICT(asset_name) 
        DO UPDATE SET quantity = quantity + 100, last_updated = excluded.last_updated
    ''', (now,))
    
    conn.commit()
    conn.close()
    print("[+] [大商會] 貿易成功！帝國金庫資產增加，當前國庫充盈。")

