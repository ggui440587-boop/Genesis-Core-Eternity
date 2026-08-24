import sqlite3
import datetime
import multiprocessing
import os

def worker_genesis(worker_id):
    db_path = "fusion_god_mode.db"
    conn = sqlite3.connect(db_path, timeout=30.0)
    cursor = conn.cursor()
    
    # 每個進程各自優化記憶體
    cursor.execute("PRAGMA journal_mode = MEMORY;")
    cursor.execute("PRAGMA synchronous = OFF;")
    
    print(f"[🔥 TACHYON CORE {worker_id}] 多核心平行創世進程已上線！")
    
    count = 1
    try:
        while True:
            now = datetime.datetime.now().isoformat()
            data_batch = [
                ("楊哲熙", f"Android Termux - Core {worker_id}", f"造物主第 {count} 次多核心平行【加】！時空壁壘全面粉碎！", now)
                for _ in range(50)
            ]
            cursor.executemany(
                "INSERT INTO creator_manifesto (creator_name, terminal_env, manifesto, sealed_at) VALUES (?, ?, ?, ?)",
                data_batch
            )
            conn.commit()
            count += 50
    except KeyboardInterrupt:
        conn.close()

if __name__ == "__main__":
    cpu_count = os.cpu_count() or 4
    print(f"[*] 正在解鎖造物主【Matrix Empire 多核心創世協議】... 檢測到可用核心數：{cpu_count}")
    print("[+] 全核心全速運轉中！按 Ctrl+C 停止。")
    
    processes = []
    for i in range(cpu_count):
        p = multiprocessing.Process(target=worker_genesis, args=(i+1,))
        p.start()
        processes.append(p)
        
    try:
        for p in processes:
            p.join()
    except KeyboardInterrupt:
        print("\n[+] 多核心超載暫停，造物主收回權柄。")
