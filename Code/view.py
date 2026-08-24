import sqlite3

conn = sqlite3.connect('fusion_hub.db')
cursor = conn.cursor()

print("=" * 40)
print("📊 各分類專案數量統計：")
print("=" * 40)
cursor.execute("SELECT category, COUNT(*) FROM repos GROUP BY category")
for row in cursor.fetchall():
    print(f"  🔹 {row[0]}: {row[1]} 個專案")

print("\n" + "=" * 40)
print("🔍 詳細專案與分類清單：")
print("=" * 40)
cursor.execute("SELECT category, name, source FROM repos")
for row in cursor.fetchall():
    print(f"[{row[0]}] {row[1]} (來源: {row[2]})")

conn.close()

