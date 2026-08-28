import sqlite3
from datetime import datetime

TIER = 2  # 邊境與勞動階級

def run(db_name):
    print("[-] [邊境拓荒司] 正在調度奴隸與自由民開墾新領土...")
    territory = "Sector-Termux-Omega"
    ruler = "Duke of Omega"
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT OR IGNORE INTO empire_domains (territory_name, ruler_title, citizens_count, slaves_count, status, annexed_at)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (territory, ruler, 2000, 800, "PROSPEROUS", now))
    
    conn.commit()
    conn.close()
    print(f"[+] [拓荒司] 領地「{territory}」開發完畢：容納 2000 名自由民與 800 名奴隸勞動力。")

