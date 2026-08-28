import sqlite3
from datetime import datetime

TIER = 1  # 皇帝直屬暗部

def run(db_name):
    print("[-] [祕密警察/暗部] 正在審查全境臣屬忠誠度與系統異常...")
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO secret_police_records (target_module, crime_action, penalty, executed_at)
        VALUES ('All_Modules', 'Routine_Loyalty_Check', 'CLEAN', ?)
    ''', (now,))
    conn.commit()
    conn.close()
    print("[+] [暗部總管] 皇城內外肅靜，無人敢有異心，絕對服從皇帝陛下。")

