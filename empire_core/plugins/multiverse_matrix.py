import sqlite3
import random
from datetime import datetime

TIER = 1  # 宇宙創世階級

def run(db_name):
    print("[-] [多元宇宙矩陣] 正在運算 1,024 個平行微型宇宙之演化進程...")
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # 平行宇宙產生的能量與算力收益
    cosmic_energy = random.randint(1000, 5000)
    
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO imperial_treasury (asset_name, quantity, last_updated)
        VALUES ('Cosmic_Matrix_Energy', ?, ?)
        ON CONFLICT(asset_name) 
        DO UPDATE SET quantity = quantity + ?, last_updated = excluded.last_updated
    ''', (cosmic_energy, now, cosmic_energy))
    
    cursor.execute('''
        INSERT INTO imperial_chronicles (era_version, event_type, description, recorded_at)
        VALUES ('v3.0-Eternal', 'MULTIVERSE_HARVEST', f'多元宇宙矩陣收割：獲得平行宇宙能量 {cosmic_energy} 單位。', ?)
    ''', (now,))
    
    conn.commit()
    conn.close()
    print(f"[+] [多元宇宙矩陣] 能量汲取完成：成功收割 {cosmic_energy} 單位創世算力。")

