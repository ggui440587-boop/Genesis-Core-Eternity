import sqlite3

def run():
    print("[-] [test_intel] 正在執行情報擴充模組...")
    # 這裡可以寫你的爬蟲或資料處理邏輯
    # 示範直接寫入資料庫
    conn = sqlite3.connect('../fusion_hub.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS intel_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT
        )
    ''')
    cursor.execute("INSERT INTO intel_data (content) VALUES ('測試情報：自動擴充模組運行正常')")
    conn.commit()
    conn.close()
    print("[+] [test_intel] 情報寫入成功！")

