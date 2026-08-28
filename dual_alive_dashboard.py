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

# 雙軌獨立生命狀態
TRACK_STATE = {
    "precision": {
        "is_paused": False,
        "heartbeat": 0,
        "status": "左側精準育種室：待命...",
        "energy": 100
    },
    "wild": {
        "is_paused": False,
        "heartbeat": 0,
        "status": "右側野生突變區：待命...",
        "energy": 100
    }
}

# ==================== 左側產線獨立背景執行緒 ====================
def precision_organism_loop():
    global TRACK_STATE
    directions = ["AI agent", "python security", "data parser"]
    
    while True:
        state = TRACK_STATE["precision"]
        if state["is_paused"]:
            state["status"] = "【左側】已進入冬眠休眠..."
            time.sleep(1)
            continue
            
        try:
            state["heartbeat"] += 1
            query = random.choice(directions)
            state["status"] = f"【左側精準】正在嚴格檢驗: {query}"
            
            url = f"https://api.github.com/search/repositories?q={urllib.request.quote(query)}+language:python&sort=stars&order=desc"
            req = urllib.request.Request(url, headers={'User-Agent': 'Precision-Lab', 'Accept': 'application/vnd.github.v3+json'})
            
            with urllib.request.urlopen(req, timeout=8) as response:
                result = json.loads(response.read().decode('utf-8'))
                items = result.get("items", [])[:1]
                if items:
                    item = items[0]
                    p_file = PRECISION_DIR / f"{item['name']}.json"
                    if item.get("stargazers_count", 0) > 10:
                        p_file.write_text(json.dumps(item), encoding="utf-8")
                        state["energy"] = min(150, state["energy"] + 3)
                        state["status"] = f"【左側精準】合格！收編: {item['name']}"
                    else:
                        if p_file.exists(): p_file.unlink()
                        state["energy"] = max(20, state["energy"] - 2)
                        state["status"] = f"【左側精準】不合格，已銷毀殘骸"
            time.sleep(7)
        except Exception as e:
            state["status"] = f"【左側】防護罩隔離異常"
            time.sleep(4)

# ==================== 右側產線獨立背景執行緒 ====================
def wild_organism_loop():
    global TRACK_STATE
    directions = ["chaos engineering", "fuzzy test", "neural mutation"]
    
    while True:
        state = TRACK_STATE["wild"]
        if state["is_paused"]:
            state["status"] = "【右側】已進入冬眠休眠..."
            time.sleep(1)
            continue
            
        try:
            state["heartbeat"] += 1
            query = random.choice(directions)
            state["status"] = f"【右側野生】正在盲撞突變: {query}"
            
            url = f"https://api.github.com/search/repositories?q={urllib.request.quote(query)}+language:python&sort=stars&order=desc"
            req = urllib.request.Request(url, headers={'User-Agent': 'Wild-Lab', 'Accept': 'application/vnd.github.v3+json'})
            
            with urllib.request.urlopen(req, timeout=8) as response:
                result = json.loads(response.read().decode('utf-8'))
                items = result.get("items", [])[:2]
                if len(items) >= 2:
                    chimera = f"{items[0]['name']}_X_WILD"
                    w_file = WILD_DIR / f"{chimera}.txt"
                    if random.random() < 0.8:
                        w_file.write_text(f"Mutated: {chimera}", encoding="utf-8")
                        state["energy"] = min(150, state["energy"] + 5)
                        state["status"] = f"【右側野生】誕生新混血: {chimera}"
                    else:
                        if w_file.exists(): w_file.unlink()
                        state["energy"] = max(20, state["energy"] - 3)
                        state["status"] = f"【右側野生】基因崩潰，當場銷毀"
            time.sleep(6)
        except Exception as e:
            state["status"] = f"【右側】野生亂流隔離中"
            time.sleep(4)

# ==================== 雙軌網頁面版介面 ====================
class DualDashboardHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        query_params = parse_qs(parsed_path.query)
        
        # 獨立控制左側或右側的暫停／恢復
        if "track" in query_params and "action" in query_params:
            track = query_params["track"][0]
            action = query_params["action"][0]
            if track in TRACK_STATE:
                if action == "pause":
                    TRACK_STATE[track]["is_paused"] = True
                elif action == "resume":
                    TRACK_STATE[track]["is_paused"] = False

        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        
        p = TRACK_STATE["precision"]
        w = TRACK_STATE["wild"]
        
        # 樣式判斷
        p_core = "background: radial-gradient(circle, #ffaa00 0%, #663300 100%); box-shadow: 0 0 20px #ffaa00; animation: none;" if p["is_paused"] else "background: radial-gradient(circle, #00ccff 0%, #004466 100%); box-shadow: 0 0 25px #00ccff; animation: hb-p 1.5s infinite;"
        w_core = "background: radial-gradient(circle, #ffaa00 0%, #663300 100%); box-shadow: 0 0 20px #ffaa00; animation: none;" if w["is_paused"] else "background: radial-gradient(circle, #ff007f 0%, #660033 100%); box-shadow: 0 0 25px #ff007f; animation: hb-w 1.2s infinite;"
        
        p_btn_action, p_btn_text, p_btn_color = ("resume", "喚醒左側", "#00ccff") if p["is_paused"] else ("pause", "暫停左側", "#ffbb00")
        w_btn_action, w_btn_text, w_btn_color = ("resume", "喚醒右側", "#ff007f") if w["is_paused"] else ("pause", "暫停右側", "#ffbb00")

        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <title>Genesis Dual-Track Bio-Lab</title>
            <style>
                body {{
                    background: #08080c;
                    color: #fff;
                    font-family: monospace;
                    margin: 0;
                    padding: 15px;
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                }}
                h2 {{ margin-bottom: 20px; color: #00ffcc; text-shadow: 0 0 10px rgba(0,255,204,0.3); }}
                .container {{
                    display: flex;
                    flex-direction: column;
                    gap: 20px;
                    width: 100%;
                    max-width: 400px;
                }}
                .dish-card {{
                    background: rgba(20, 20, 30, 0.9);
                    border: 1px solid rgba(255,255,255,0.1);
                    border-radius: 14px;
                    padding: 15px;
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    box-shadow: 0 4px 15px rgba(0,0,0,0.5);
                }}
                .petri {{
                    width: 140px;
                    height: 140px;
                    border-radius: 50%;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    margin-bottom: 12px;
                    border: 2px dashed rgba(255,255,255,0.2);
                }}
                .core {{ width: 50px; height: 50px; border-radius: 50%; }}
                @keyframes hb-p {{ 0%,100%{{transform:scale(0.9);}} 50%{{transform:scale(1.1);}} }}
                @keyframes hb-w {{ 0%,100%{{transform:scale(0.85);}} 50%{{transform:scale(1.15);}} }}
                
                .info {{ font-size: 12px; text-align: center; margin-bottom: 10px; }}
                .msg {{ color: #ffbb00; font-size: 11px; margin-top: 5px; height: 30px; text-align: center; }}
                
                .btn {{
                    background: var(--bg-color);
                    color: #08080c;
                    border: none;
                    padding: 8px 20px;
                    font-size: 13px;
                    font-weight: bold;
                    border-radius: 20px;
                    cursor: pointer;
                    text-decoration: none;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.3);
                }}
            </style>
            <meta http-equiv="refresh" content="3">
        </head>
        <body>
            <h2>⚡ 雙軌獨立生物實驗室</h2>
            
            <div class="container">
                <!-- 左側精準育種區 -->
                <div class="dish-card" style="border-color: #00ccff55;">
                    <h3 style="color: #00ccff; margin: 0 0 10px 0;">🔵 左側：精準育種室</h3>
                    <div class="dish-card-inner">
                        <div class="petri" style="border-color: #00ccff44;">
                            <div class="core" style="{p_core}"></div>
                        </div>
                    </div>
                    <div class="info">心跳: #{p['heartbeat']} | 能量: {p['energy']} EP</div>
                    <div class="msg">{p['status']}</div>
                    <a class="btn" style="background: {p_btn_color};" href="/?track=precision&action={p_btn_action}">{p_btn_text}</a>
                </div>

                <!-- 右側野生突變區 -->
                <div class="dish-card" style="border-color: #ff007f55;">
                    <h3 style="color: #ff007f; margin: 0 0 10px 0;">🟣 右側：野生突變區</h3>
                    <div class="dish-card-inner">
                        <div class="petri" style="border-color: #ff007f44;">
                            <div class="core" style="{w_core}"></div>
                        </div>
                    </div>
                    <div class="info">心跳: #{w['heartbeat']} | 能量: {w['energy']} EP</div>
                    <div class="msg">{w['status']}</div>
                    <a class="btn" style="background: {w_btn_color};" href="/?track=wild&action={w_btn_action}">{w_btn_text}</a>
                </div>
            </div>
        </body>
        </html>
        """
        self.wfile.write(html.encode("utf-8"))

if __name__ == "__main__":
    # 啟動雙軌獨立執行緒
    threading.Thread(target=precision_organism_loop, daemon=True).start()
    threading.Thread(target=wild_organism_loop, daemon=True).start()
    
    server = HTTPServer(('127.0.0.1', 8080), DualDashboardHandler)
    print("⚡ 雙軌獨立面板已啟動！請在瀏覽器打開: http://127.0.0.1:8080")
    server.serve_forever()
