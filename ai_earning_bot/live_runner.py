import time
import threading
import sqlite3
import datetime
import pathlib

DB_PATH = "live_runtime.db"
LOG_PATH = "live_output.log"
# 控制背景執行緒開關的旗標
is_running = True

def init_database():
    """初始化真實的 SQLite 資料庫與表格"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS runtime_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_name TEXT,
            status TEXT,
            created_at TEXT
        )
    """)
    conn.commit()
    conn.close()

def log_message(message):
    """將即時訊息寫入終端機與實體日誌檔案"""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"[{timestamp}] {message}\n"
    print(log_line.strip())
    # 限制日誌過大的簡單防護：實際開發可加入大小檢查
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(log_line)

def background_worker():
    """優化後的背景迴圈工作執行緒"""
    init_database()
    log_message("🚀 [背景守護] 系統已成功啟動，開始進行即時循環運作...")
    
    counter = 1
    global is_running
    
    # 建立單一連線或在迴圈內安全管理
    while is_running:
        try:
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # 使用更安全的 Context Manager (with 語法) 自動關閉連線
            with sqlite3.connect(DB_PATH) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO runtime_events (event_name, status, created_at) VALUES (?, ?, ?)",
                    (f"Heartbeat-Cycle-{counter}", "active_running", current_time)
                )
                conn.commit()
            
            log_message(f"✨ [循環成功] 已完成第 {counter} 次背景資料寫入與狀態更新。")
            counter += 1
            
            # 分段睡眠以支援快速回應關閉訊號
            for _ in range(5):
                if not is_running:
                    break
                time.sleep(1)
                
        except Exception as e:
            log_message(f"❌ [錯誤發生] 背景運行例外: {e}")
            time.sleep(3)

if __name__ == "__main__":
    worker_thread = threading.Thread(target=background_worker, daemon=True)
    worker_thread.start()
    
    log_message("📌 主程序已進入守護狀態，按下 Ctrl+C 可安全退出。")
    
    try:
        while worker_thread.is_alive():
            time.sleep(0.5)
    except KeyboardInterrupt:
        log_message("🛑 收到終止訊號，正在安全關閉背景守護程式...")
        is_running = False
        worker_thread.join(timeout=2)
        log_message("👋 程式已完全安全退出。")
