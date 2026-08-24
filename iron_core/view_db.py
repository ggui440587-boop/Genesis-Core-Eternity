import sqlite3

def view_feed():
    conn = sqlite3.connect("fusion_hub.db")
    cursor = conn.cursor()
    cursor.execute("SELECT source, title, ai_summary, processed_at FROM processed_items ORDER BY processed_at DESC LIMIT 10")
    rows = cursor.fetchall()
    conn.close()

    print("\n" + "="*40)
    print(" 🧠 你的 AI 大腦戰利品清單 (最近 10 筆)")
    print("="*40)
    for idx, row in enumerate(rows, 1):
        print(f"[{idx}] 來源: {row[0]} | 時間: {row[3]}")
        print(f"📌 標題: {row[1]}")
        print(f"💡 摘要: {row[2]}")
        print("-" * 40)

if __name__ == "__main__":
    view_feed()
