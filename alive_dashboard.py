import urllib.request
import json
import random
import time
import threading
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse

BASE_DIR = Path("./")
PRECISION_DIR = BASE_DIR / "species_precision"
WILD_DIR = BASE_DIR / "species_wild"

PRECISION_DIR.mkdir(exist_ok=True)
WILD_DIR.mkdir(exist_ok=True)

# 系統生物狀態與開關
BIO_STATE = {
    "heartbeat": 0,
    "is_paused": False,  # 預設運作中
    "status_msg": "培養皿正在甦醒...",
    "energy": 100
}

def background_organism():
    global BIO_STATE
    directions = ["AI agent", "neural network", "python spider", "quantum logic", "auto synthesizer"]
    
    while True:
        # 如果被暫停，則進入休眠等待，不消耗資源、不對外捕食
        if BIO_STATE["is_paused"]:
            BIO_STATE["status_msg"] = "狀態：已進入冬眠暫停（保留能量中）..."
            time.sleep(1)
            continue

        try:
            BIO_STATE["heartbeat"] += 1
            query = random.choice(directions)
            BIO_STATE["status_msg"] = f"正在外部捕食關鍵字: [{query}]"
            
            url = f"https://api.github.com/search/repositories?q={urllib.request.quote(query)}+language:python&sort=stars&order=desc"
            req = urllib.request.Request(url, headers={'User-Agent': 'Bio-Organism-Core', 'Accept': 'application/vnd.github.v3+json'})
            
            with urllib.request.urlopen(req, timeout=8) as response:
                result = json.loads(response.read().decode('utf-8'))
                items = result.get("items", [])[:2]
                
                if len(items) >= 2:
                    # 左側細胞（精準育種）
                    item_a = items[0]
                    p_file = PRECISION_DIR / f"{item_a['name']}.json"
                    if item_a.get("stargazers_count", 0) > 5:
                        p_file.write_text(json.dumps(item_a), encoding="utf-8")
                        BIO_STATE["energy"] = min(150, BIO_STATE["energy"] + 5)
                    else:
                        if p_file.exists(): p_file.unlink()
                        BIO_STATE["energy"] = max(20, BIO_STATE["energy"] - 2)
                    
                    # 右側野獸（野生突變）
                    item_b = items[1]
                    chimera = f"{item_a['name']}_X_{item_b['name']}"
                    w_file = WILD_DIR / f"{chimera}.txt"
                    if random.random() < 0.75:
                        w_file.write_text(f"Mutated life: {chimera}", encoding="utf-8")
                    else:
                        if w_file.exists(): w_file.unlink()
                        
            time.sleep(6)
        except Exception as e:
            BIO_STATE["status_msg"] = f"環境波動（異常已被生物膜隔離）"
            time.sleep(4)

class AliveDashboardHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        query_params = parse_qs(parsed_path.query)
        
        # 處理暫停／恢復指令
        if "action" in query_params:
            cmd = query_params["action"][0]
            if cmd == "pause":
                BIO_STATE["is_paused"] = True
            elif cmd == "resume":
                BIO_STATE["is_paused"] = False
                
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        
        # 依據目前狀態改變核心顏色（暫停時變暗、運作時發光）
        core_style = "background: radial-gradient(circle, #ffaa00 0%, #663300 100%); box-shadow: 0 0 25px #ffaa00; animation: none;" if BIO_STATE["is_paused"] else "background: radial-gradient(circle, #00ffcc 0%, #006644 100%); box-shadow: 0 0 25px #00ffcc; animation: heartbeat 1.5s ease-in-out infinite;"
        dish_style = "border: 3px solid rgba(255, 170, 0, 0.4); box-shadow: 0 0 30px rgba(255, 170, 0, 0.15) inset;" if BIO_STATE["is_paused"] else "border: 3px solid rgba(0, 255, 204, 0.4); box-shadow: 0 0 30px rgba(0, 255, 204, 0.15) inset, 0 0 20px rgba(0, 255, 204, 0.2);"
        
        # 切換按鈕文字與網址
        btn_action = "resume" if BIO_STATE["is_paused"] else "pause"
        btn_text = "喚醒 / 繼續運作" if BIO_STATE["is_paused"] else "暫停 / 進入冬眠"
        btn_color = "#00ffcc" if BIO_STATE["is_paused"] else "#ffbb00"

        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <title>Genesis Bio-Lab</title>
            <style>
                body {{
                    background: #08080c;
                    color: #00ffcc;
                    font-family: monospace;
                    margin: 0;
                    padding: 20px;
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    min-height: 100vh;
                    overflow-x: hidden;
                }}
                .petri-dish {{
                    width: 280px;
                    height: 280px;
                    border-radius: 50%;
                    position: relative;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    animation: pulse-dish 4s ease-in-out infinite;
                    margin-bottom: 25px;
                    {dish_style}
                }}
                @keyframes pulse-dish {{
                    0%, 100% {{ transform: scale(1); }}
                    50% {{ transform: scale(1.02); }}
                }}
                .core-nucleus {{
                    width: 70px;
                    height: 70px;
                    border-radius: 50%;
                    {core_style}
                }}
                @keyframes heartbeat {{
                    0%, 100% {{ transform: scale(0.9); opacity: 0.8; }}
                    50% {{ transform: scale(1.15); opacity: 1; box-shadow: 0 0 40px #00ffcc; }}
                }}
                .bio-stats {{
                    background: rgba(20, 20, 30, 0.8);
                    border: 1px solid rgba(0, 255, 204, 0.3);
                    padding: 15px 20px;
                    border-radius: 12px;
                    text-align: center;
                    width: 85%;
                    max-width: 350px;
                    box-shadow: 0 4px 15px rgba(0,0,0,0.5);
                    margin-bottom: 20px;
                }}
                .status-text {{ color: #ffbb00; font-size: 13px; margin-top: 8px; }}
                .btn {{
                    background: {btn_color};
                    color: #08080c;
                    border: none;
                    padding: 12px 25px;
                    font-size: 15px;
                    font-weight: bold;
                    border-radius: 25px;
                    cursor: pointer;
                    text-decoration: none;
                    box-shadow: 0 4px 10px rgba(0,0,0,0.4);
                    transition: 0.2s;
                }}
                .btn:active {{ transform: scale(0.95); }}
            </style>
            <meta http-equiv="refresh" content="3">
        </head>
        <body>
            <h2>🧬 雙軌基因與細胞培養皿</h2>
            
            <div class="petri-dish">
                <div class="core-nucleus" title="核心生命體"></div>
            </div>
            
            <div class="bio-stats">
                <div>脈衝心跳: <b>#{BIO_STATE['heartbeat']}</b> | 能量: <b>{BIO_STATE['energy']} EP</b></div>
                <div class="status-text">{BIO_STATE['status_msg']}</div>
            </div>

            <a class="btn" href="/?action={btn_action}">{btn_text}</a>
        </body>
        </html>
        """
        self.wfile.write(html.encode("utf-8"))

if __name__ == "__main__":
    t = threading.Thread(target=background_organism, daemon=True)
    t.start()
    
    server = HTTPServer(('127.0.0.1', 8080), AliveDashboardHandler)
    print("🧬 具備暫停開關的生物面板已啟動！請在瀏覽器打開: http://127.0.0.1:8080")
    server.serve_forever()
