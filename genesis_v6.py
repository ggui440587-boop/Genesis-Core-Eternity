import sqlite3
import datetime

DB_PATH = "genesis_core.db"
WAR_ROOM_PATH = "war_room.md"

def expand_matrix_v6():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 確保資料庫有跨界融合與實體邊陲的擴張表格
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS fringe_matrix (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            domain TEXT, concept TEXT, node_status TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # 注入實體邊陲與非數位人文的動態節點
    fringe_assets = [
        ("Urban-Artifact", "高圓寺無名信箱：零權威實體獨立刊物交換", "Active-Offline"),
        ("Acoustic-Ecology", "太平洋自然原音極低頻黑膠留存計畫", "Active-Isolated"),
        ("Mechanical-Heritage", "19世紀無動力自平衡重力機械檔案", "Archived-Pure")
    ]
    
    new_fringe_count = 0
    for domain, concept, status in fringe_assets:
        # 檢查是否已存在該概念，避免重複
        cursor.execute('SELECT id FROM fringe_matrix WHERE concept = ?', (concept,))
        if cursor.fetchone():
            continue
        cursor.execute('INSERT INTO fringe_matrix (domain, concept, node_status) VALUES (?, ?, ?)',
                       (domain, concept, status))
        new_fringe_count += 1
        
    conn.commit()
    
    # 讀取數位端與實體端最新資產進行矩陣聯動
    cursor.execute('SELECT cleaned_content FROM processed_assets ORDER BY id DESC LIMIT 4')
    digital_rows = cursor.fetchall()
    
    cursor.execute('SELECT domain, concept, node_status FROM fringe_matrix ORDER BY id DESC LIMIT 3')
    fringe_rows = cursor.fetchall()
    
    conn.close()
    
    # 戰情室全面升級版 v6：雙軌並行（數位程式脈動 + 實體邊陲哲學）
    report = f"# 🌐 Genesis-Matrix 終極全域戰情室 (v6)\n"
    report += f"> **全域同步時間**：{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    report += f"> **矩陣擴張狀態**：數位引擎與實體邊陲雷達已雙向鎖定\n\n---\n\n"
    
    report += "## ⚡ [軌道一] 數位與代碼核心資產\n"
    if digital_rows:
        for r in digital_rows:
            report += f"{r[0]}\n\n---\n\n"
    else:
        report += "- 尚無數位暫存資產。\n\n---\n\n"
        
    report += "## 🌿 [軌道二] 實體邊陲與次文化動態\n"
    for domain, concept, status in fringe_rows:
        report += f"### 🗺️ [{domain}] {concept}\n"
        report += f"- **節點狀態**: `{status}`\n"
        report += f"- **同步頻率**: 脫離演算法干擾，維持純粹離線自主運作 [Timestamp: {datetime.datetime.now().strftime('%H:%M:%S')}]\n\n---\n\n"
        
    with open(WAR_ROOM_PATH, "w", encoding="utf-8") as f:
        f.write(report)
        
    print(f"[Genesis-Matrix v6] 雙軌擴張完畢！新增實體邊陲節點：{new_fringe_count} 筆。戰情室已全面更新至：{WAR_ROOM_PATH}")

if __name__ == "__main__":
    expand_matrix_v6()
