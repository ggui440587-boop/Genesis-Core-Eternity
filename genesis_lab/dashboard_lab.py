import urllib.request
import json
import random
import time
import threading
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler

BASE_DIR = Path("./")
PRECISION_DIR = BASE_DIR / "species_precision"
WILD_DIR = BASE_DIR / "species_wild"

PRECISION_DIR.mkdir(exist_ok=True)
WILD_DIR.mkdir(exist_ok=True)

# 狀態紀錄器（供面板即時讀取）
SYSTEM_STATUS = {
    "last_action": "系統剛啟動，正在初始化...",
    "active_directions": ["AI agent", "python automation", "web scraper"],
    "survived_count": 0,
    "destroyed_count": 0
}

# ==================== 1. 背景自主探索核心 ====================
def background_explorer():
    global SYSTEM_STATUS
    directions = SYSTEM_STATUS["active_directions"]
    
    while True:
        try:
            query = random.choice(directions)
            SYSTEM_STATUS["last_action"] = f"正在外部獵取方向: {query}"
            
            url = f"https://api.github.com/search/repositories?q={urllib.request.quote(query)}+language:python&sort=stars&order=desc"
            req = urllib.request.Request(url, headers={'User-Agent': 'Genesis-Dashboard-Bot', 'Accept': 'application/vnd.github.v3+json'})
            
            with urllib.request.urlopen(req, timeout=10) as response:
                result = json.loads(response.read().decode('utf-8'))
                items = result.get("items", [])[:2]
                
                if len(items) >= 2:
                    # 左側精準育種
                    item_a = items[0]
                    is_valid = item_a.get("stargazers_count", 0) > 10
                    p_file = PRECISION_DIR / f"{item_a['name']}.json"
                    if is_valid:
                        p_file.write_text(json.dumps(item_a, indent=2), encoding="utf-8")
                        SYSTEM_STATUS["survived_count"] += 1
                        SYSTEM_STATUS["last_action"] = f"【左側精準生存】存入: {item_a['name']}"
                    else:
                        if p_file.exists(): p_file.unlink()
                        SYSTEM_STATUS["destroyed_count"] += 1
                        SYSTEM_STATUS["last_action"] = f"【左側精準銷毀】清除: {item_a['name']}"
                    
                    # 右側野生盲撞
                    item_b = items[1]
                    chimera = f"{item_a['name']}_X_{item_b['name']}"
                    w_file = WILD_DIR / f"{chimera}.txt"
                    if random.random() < 0.8:
                        w_file.write_text(f"Hybrid: {item_a['name']} + {item_b['name']}", encoding="utf-8")
                        SYSTEM_STATUS["survived_count"] += 1
                        SYSTEM_STATUS["last_action"] = f"【右側野生突變】誕生: {chimera}"
                    else:
                        if w_file.exists(): w_file.unlink()
                        SYSTEM_STATUS["destroyed_count"] += 1
                        SYSTEM_STATUS["last_action"] = f"【右側野生崩潰】銷毀殘骸"
                        
            time.sleep(10)
        except Exception as e:
            SYSTEM_STATUS["last_action"] = f"探索過程發生例外: {str(e)}"
            time.sleep(5)

# ==================== 2. 輕量即時網頁面板伺服器 ====================
class SimpleDashboardHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        
        # 讀取當前資料夾下的所有成果
        precision_files = [f.name for f in PRECISION_DIR.glob("*.json")]
        wild_files = [f.name for f in WILD_DIR.glob("*.txt")]
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <title>Genesis Dual-Track Dashboard</title>
            <meta http-equiv="refresh" content="3"> <!-- 每 3 秒自動重新整理即時面板 -->
            <style>
                body {{ background: #121212; color: #00ffcc; font-family: monospace; padding: 20px; }}
                h1, h2 {{ border-bottom: 1px solid #333; padding-bottom: 5px; }}
                .card {{ background: #1e1e1e; padding: 15px; margin-bottom: 15px; border-radius: 8px; border: 1px solid #333; }}
                .status {{ color: #ffcc00; font-weight: bold; }}
                ul {{ padding-left: 20px; }}
                li {{ color: #ccc; margin-bottom: 5px; }}
            </style>
        </head>
        <body>
            <h1>⚡ 雙軌自治實驗室 - 即時面板</h1>
            
            <div class="card">
                <h2>系統即時狀態</h2>
                <p>最近動作：<span class="status">{SYSTEM_STATUS['last_action']}</span></p>
                <p>生存總數：{SYSTEM_STATUS['survived_count']} | 銷毀總數：{SYSTEM_STATUS['destroyed_count']}</p>
            </div>
            
            <div class="card">
                <h2>左側：精準育種庫 ({len(precision_files)})</h2>
                <ul>{''.join([f"<li>{f}</li>" for f in precision_files]) or '<li>尚無存活樣本</li>'}</ul>
            </div>
            
            <div class="card">
                <h2>右側：野生突變區 ({len(wild_files)})</h2>
                <ul>{''.join([f"<li>{f}</li>" for f in wild_files]) or '<li>尚無混血物種</li>'}</ul>
            </div>
            
            <p style="color: #666; font-size: 12px;">提示：此面板每 3 秒自動更新一次。關閉終端機可透過背景程序維持。</p>
        </body>
        </html>
        """
        self.wfile.write(html.encode("utf-8"))

def run_server():
    server = HTTPServer(('127.0.0.1', 8080), SimpleDashboardHandler)
    print("🌐 即時面板已啟動！請在瀏覽器打開: http://127.0.0.1:8080")
    server.serve_forever()

if __name__ == "__main__":
    # 啟動背景探索執行緒
    t = threading.Thread(target=background_explorer, daemon=True)
    t.start()
    
    # 啟動網頁面板伺服器
    run_server()
