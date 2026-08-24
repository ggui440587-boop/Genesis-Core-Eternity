import importlib.util
import types
import sqlite3
import datetime

print("[*] 正在載入造物主【多態自我演化引擎】...")

def generate_dynamic_parser(target_type):
    if target_type == "article":
        return """
def parse_unknown_target(raw_html):
    return {
        "title": "AI 深度演化：文章類目標",
        "content": "成功萃取文章主體與結構化數據。",
        "category": "Article"
    }
"""
    elif target_type == "api":
        return """
def parse_unknown_target(raw_html):
    return {
        "title": "AI 深度演化：API 介面目標",
        "content": "成功攔截並反向解析未知 JSON 酬載。",
        "category": "API"
    }
"""
    else:
        return """
def parse_unknown_target(raw_html):
    return {
        "title": "AI 深度演化：未知多維獵物",
        "content": "透過動態腳本捕獲並清洗流動數據。",
        "category": "Generic"
    }
"""

def init_db():
    conn = sqlite3.connect("fusion_hub.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS evolution_targets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            content TEXT,
            category TEXT,
            created_at TEXT
        )
    """)
    conn.commit()
    return conn

def multi_evolve_and_execute():
    conn = init_db()
    cursor = conn.cursor()
    
    target_types = ["article", "api", "generic"]
    
    for t_type in target_types:
        dynamic_code = generate_dynamic_parser(t_type)
        dyn_module = types.ModuleType(f"dynamic_parser_{t_type}")
        exec(dynamic_code, dyn_module.__dict__)
        
        result = dyn_module.parse_unknown_target(f"<html>Sample {t_type} HTML</html>")
        
        now = datetime.datetime.now().isoformat()
        cursor.execute(
            "INSERT INTO evolution_targets (title, content, category, created_at) VALUES (?, ?, ?, ?)",
            (result["title"], result["content"], result["category"], now)
        )
    
    conn.commit()
    conn.close()
    print("[+] 🧬 多態自我演化完畢！多重獵物已全面寫入 fusion_hub.db。")

def query_all_targets():
    conn = sqlite3.connect("fusion_hub.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, category, created_at FROM evolution_targets ORDER BY id DESC LIMIT 5")
    rows = cursor.fetchall()
    print("\n[🔍 資料庫最近 5 筆動態獵物清單]")
    for row in rows:
        print(f"  ID: {row[0]} | 標題: {row[1]} | 分類: {row[2]} | 時間: {row[3]}")
    conn.close()

if __name__ == "__main__":
    multi_evolve_and_execute()
    query_all_targets()
