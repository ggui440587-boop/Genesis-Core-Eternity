import sqlite3
import os
import time

DB_FILE = "matrix_society.db"

def show_dashboard():
    if not os.path.exists(DB_FILE):
        print("[!] 尚未找到社會矩陣資料庫 (matrix_society.db)，請先執行 full_society.py。")
        return

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # 清除終端機畫面以達到即時更新效果
    os.system('clear' if os.name == 'posix' else 'cls')

    print("=" * 70)
    print("         🌐 賽博社會矩陣即時儀表板 (CYBER SOCIETY DASHBOARD) 🌐")
    print("=" * 70)

    # 1. 統計總覽
    cursor.execute("SELECT COUNT(*) FROM citizens WHERE pathway != 'CRADLE'")
    total_citizens = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM citizens WHERE pathway = 'POSITIVE_PATH'")
    pos_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM citizens WHERE pathway = 'NEGATIVE_PATH'")
    neg_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM citizens WHERE pathway = 'CRADLE'")
    cradle_count = cursor.fetchone()[0]

    print(f"📊 總公民數: {total_citizens} | 🏛️ 正面秩序線: {pos_count} | 🏴‍☠️ 負面暗影線: {neg_count} | 👶 搖籃中: {cradle_count}")
    print("-" * 70)

    # 2. 顯示雙軌頂點（總統與最大黑手）
    print("👑 【雙軌最高權力中樞】")
    cursor.execute("SELECT name, profession, status FROM citizens WHERE profession IN ('President', 'Maximum_Mastermind')")
    leaders = cursor.fetchall()
    if leaders:
        for name, prof, status in leaders:
            side = "🏛️ 正面總統" if prof == 'President' else "🏴‍☠️ 負面黑手"
            print(f"   ➔ [{side}] {name} ({prof}) -> {status}")
    else:
        print("   (頂點尚未誕生或選出)")

    print("-" * 70)

    # 3. 最近活動帳本
    print("📜 【最新社會行為記錄 (Ledger)】")
    cursor.execute("SELECT pathway, profession, action, status, timestamp FROM ledger ORDER BY id DESC LIMIT 6")
    logs = cursor.fetchall()
    for pathway, prof, action, status, ts in logs:
        line_icon = " [+] " if pathway == 'POSITIVE_PATH' else " [-] "
        print(f"{line_icon} [{ts}] {prof}: {action} (狀態: {status})")

    print("=" * 70)
    print("提示: 按 Ctrl+C 離開儀表板 (背景社會將繼續運轉)")
    conn.close()

if __name__ == "__main__":
    try:
        while True:
            show_dashboard()
            time.sleep(3)  # 每 3 秒重新整理一次儀表板
    except KeyboardInterrupt:
        print("\n[*] 已退出儀表板。")

