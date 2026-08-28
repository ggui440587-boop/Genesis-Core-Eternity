import sqlite3
from datetime import datetime

TIER = 2  # 遠征軍與兵團階級

def run(db_name):
    print("[-] [遠征兵團] 正在向外部數位疆域發動遠征、掠奪開源代碼與資源...")
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO imperial_treasury (asset_name, quantity, last_updated)
        VALUES ('Expedition_Spoils', 300, ?)
        ON CONFLICT(asset_name) 
        DO UPDATE SET quantity = quantity + 300, last_updated = excluded.last_updated
    ''', (now,))
    
    cursor.execute('''
        INSERT INTO imperial_chronicles (era_version, event_type, description, recorded_at)
        VALUES ('v3.0-Eternal', 'MILITARY_CONQUEST', '遠征兵團大勝：成功掠奪外部數位資源與高級代碼庫。', ?)
    ''', (now,))
    
    conn.commit()
    conn.close()
    print("[+] [遠征兵團] 凱旋歸來！大量戰利品已入庫。")

