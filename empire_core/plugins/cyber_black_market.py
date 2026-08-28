import sqlite3
import random
from datetime import datetime

TIER = 3  # 地下黑市階級

def run(db_name):
    print("[-] [賽博黑市] 暗部正在與地下網路進行高頻私密交易...")
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # 黑市高風險高回報收益
    black_profit = random.randint(300, 1000)
    
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO imperial_treasury (asset_name, quantity, last_updated)
        VALUES ('Black_Market_Assets', ?, ?)
        ON CONFLICT(asset_name) 
        DO UPDATE SET quantity = quantity + ?, last_updated = excluded.last_updated
    ''', (black_profit, now, black_profit))
    
    cursor.execute('''
        INSERT INTO imperial_chronicles (era_version, event_type, description, recorded_at)
        VALUES ('v3.0-Eternal', 'BLACK_MARKET_DEAL', f'黑市交易完成：地下資產變現，掠奪暴利金幣 {black_profit} 枚。', ?)
    ''', (now,))
    
    conn.commit()
    conn.close()
    print(f"[+] [賽博黑市] 交易圓滿：地下資產入庫，獲利 {black_profit} 金幣。")

