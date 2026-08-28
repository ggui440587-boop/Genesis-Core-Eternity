import sqlite3
import random
from datetime import datetime

TIER = 1  # 最高財政與印鈔階級

def run(db_name):
    print("[-] [帝國印鈔總署] 四大現實變現模組全面運轉中...")
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # 模擬四大賺錢管道的即時收益進帳
    content_revenue = random.randint(50, 200)      # 自動內容流量變現
    micro_service = random.randint(100, 300)       # 微型自動化外包服務
    quant_trade = random.randint(80, 250)          # 程式化數據套利
    affiliate_bonus = random.randint(60, 180)      # 聯盟行銷推廣分潤
    
    total_earned = content_revenue + micro_service + quant_trade + affiliate_bonus
    
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    # 將賺到的現實資產/金幣寫入國庫與財政日誌
    cursor.execute('''
        INSERT INTO imperial_treasury (asset_name, quantity, last_updated)
        VALUES ('Real_World_Mint_Revenue', ?, ?)
        ON CONFLICT(asset_name) 
        DO UPDATE SET quantity = quantity + ?, last_updated = excluded.last_updated
    ''', (total_earned, now, total_earned))
    
    report = (
        f"印鈔總署結算：內容變現(+{content_revenue}), "
        f"微型服務(+{micro_service}), "
        f"量化套利(+{quant_trade}), "
        f"聯盟推播(+{affiliate_bonus})。 "
        f"總計當期為陛下掠奪現實財富：{total_earned} 金幣。"
    )
    
    cursor.execute('''
        INSERT INTO imperial_chronicles (era_version, event_type, description, recorded_at)
        VALUES ('v3.0-Eternal', 'IMPERIAL_MINT_PROFIT', ?, ?)
    ''', (report, now))
    
    conn.commit()
    conn.close()
    print(f"[+] [印鈔總署] 財報奏報：{report}")

