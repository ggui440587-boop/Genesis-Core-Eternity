import urllib.request
import urllib.parse
import json
import random
import time
import threading
import re
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse

BASE_DIR = Path("./")
PRECISION_DIR = BASE_DIR / "web_precision"
WILD_DIR = BASE_DIR / "web_wild"

PRECISION_DIR.mkdir(exist_ok=True)
WILD_DIR.mkdir(exist_ok=True)

TRACK_STATE = {
    "precision": {
        "is_paused": False,
        "heartbeat": 0,
        "status": "多源網頁精準育種（防重過濾中）...",
        "energy": 100
    },
    "wild": {
        "is_paused": False,
        "heartbeat": 0,
        "status": "多源網頁野生盲撞...",
        "energy": 100
    }
}

def precision_crawler_loop():
    global TRACK_STATE
    seed_sources = [
        "https://news.ycombinator.com/",
        "https://www.python.org/downloads/",
        "https://github.com/trending"
    ]
    
    while True:
        state = TRACK_STATE["precision"]
        if state["is_paused"]:
            state["status"] = "【左側】已進入冬眠休眠..."
            time.sleep(1)
            continue
            
        try:
            state["heartbeat"] += 1
            target_url = random.choice(seed_sources)
            state["status"] = f"【左側爬蟲】探測中: {target_url}"
            
            req = urllib.request.Request(target_url, headers={'User-Agent': 'Mozilla/5.0 (Android; Mobile)'})
            with urllib.request.urlopen(req, timeout=10) as response:
                html_content = response.read().decode('utf-8', errors='ignore')
                urls = re.findall(r'href=[\'"]?(https?://[^\'">\s]+)', html_content)
                external_projects = [u for u in urls if any(k in u for k in ["github.com", "gitlab.com", "sourcehut", "codeberg.org"])]
                
                if external_projects:
                    chosen_url = random.choice(external_projects)
                    # 用網址雜湊或專案名稱當作唯一識別碼
                    proj_id = re.sub(r'[^a-zA-Z0-9]', '_', chosen_url.split('//')[-1])[:50]
                    p_file = PRECISION_DIR / f"{proj_id}.txt"
                    
                    # 核心防重機制：如果本地已經存在，直接銷毀重複物種
                    if p_file.exists():
                        state["status"] = f"【左側防重】發現重複專案，直接銷毀防污染"
                        state["energy"] = max(20, state["energy"] - 1)
                    elif len(chosen_url) > 20:
                        p_file.write_text(f"Unique Project: {chosen_url}", encoding="utf-8")
                        state["energy"] = min(150, state["energy"] + 4)
                        state["status"] = f"【左側精準】捕獲全新獨特專案！"
                    else:
                        if p_file.exists(): p_file.unlink()
                        state["status"] = f"【左側精準】線索不合格，已銷毀"
            time.sleep(9)
        except Exception as e:
            state["status"] = f"【左側】防護罩隔離異常"
            time.sleep(5)

def wild_crawler_loop():
    global TRACK_STATE
    while True:
        state = TRACK_STATE["wild"]
        if state["is_paused"]:
            state["status"] = "【右側】已進入冬眠休眠..."
            time.sleep(1)
            continue
            
        try:
            state["heartbeat"] += 1
            chimera_name = f"Chimera_Node_{random.randint(1000, 9999)}"
            w_file = WILD_DIR / f"{chimera_name}.txt"
            
            if random.random() < 0.75:
                w_file.write_text(f"Wild Mutation #{state['heartbeat']}", encoding="utf-8")
                state["energy"] = min(150, state["energy"] + 5)
                state["status"] = f"【右側野生】成功誕生突變物種"
            else:
                if w_file.exists(): w_file.unlink()
                state["energy"] = max(20, state["energy"] - 3)
                state["status"] = f"【右側野生】突變失敗，殘骸已銷毀"
            time.sleep(7)
        except Exception as e:
            state["status"] = f"【右側】野生亂流隔離中"
            time.sleep(5)

class CrawlerDashboardHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        query_params = parse_qs(parsed_path.query)
        
        if "track" in query_params and "action" in query_params:
            track = query_params["track"][0]
            action = query_params["action"][0]
            if track in TRACK_STATE:
                if action == "pause": TRACK_STATE[track]["is_paused"] = True
                elif action == "resume": TRACK_STATE[track]["is_paused"] = False

        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        
        p = TRACK_STATE["precision"]
        w = TRACK_STATE["wild"]
        
        p_core = "background: radial-gradient(circle, #ffaa00 0%, #663300 100%); box-shadow: 0 0 20px #ffaa00; animation: none;" if p["is_paused"] else "background: radial-gradient(circle, #00ffaa 0%, #004433 100%); box-shadow: 0 0 25px #00ffaa; animation: hb-p 1.5s infinite;"
        w_core = "background: radial-gradient(circle, #ffaa00 0%, #663300 100%); box-shadow: 0 0 20px #ffaa00; animation: none;" if w["is_paused"] else "background: radial-gradient(circle, #00aaff 0%, #002244 100%); box-shadow: 0 0 25px #00aaff; animation: hb-w 1.2s infinite;"
        
        p_btn_action, p_btn_text, p_btn_color = ("resume", "喚醒左側", "#00ffaa") if p["is_paused"] else ("pause", "暫停左側", "#ffbb00")
        w_btn_action, w_btn_text, w_btn_color = ("resume", "喚醒右側", "#00aaff") if w["is_paused"] else ("pause", "暫停右側", "#ffbb00")

        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <title>Web Crawler Bio-Lab</title>
            <style>
                body {{ background: #08080c; color: #fff; font-family: monospace; margin: 0; padding: 15px; display: flex; flex-direction: column; align-items: center; }}
                h2 {{ margin-bottom: 20px; color: #00ffaa; text-shadow: 0 0 10px rgba(0,255,170,0.3); }}
                .container {{ display: flex; flex-direction: column; gap: 20px; width: 100%; max-width: 400px; }}
                .dish-card {{ background: rgba(20, 20, 30, 0.9); border: 1px solid rgba(255,255,255,0.1); border-radius: 14px; padding: 15px; display: flex; flex-direction: column; align-items: center; box-shadow: 0 4px 15px rgba(0,0,0,0.5); }}
                .petri {{ width: 140px; height: 140px; border-radius: 50%; display: flex; justify-content: center; align-items: center; margin-bottom: 12px; border: 2px dashed rgba(255,255,255,0.2); }}
                .core {{ width: 50px; height: 50px; border-radius: 50%; }}
                @keyframes hb-p {{ 0%,100%{{transform:scale(0.9);}} 50%{{transform:scale(1.1);}} }}
                @keyframes hb-w {{ 0%,100%{{transform:scale(0.85);}} 50%{{transform:scale(1.15);}} }}
                .info {{ font-size: 12px; text-align: center; margin-bottom: 10px; }}
                .msg {{ color: #ffbb00; font-size: 11px; margin-top: 5px; height: 30px; text-align: center; }}
                .btn {{ background: var(--bg-color); color: #08080c; border: none; padding: 8px 20px; font-size: 13px; font-weight: bold; border-radius: 20px; cursor: pointer; text-decoration: none; box-shadow: 0 2px 8px rgba(0,0,0,0.3); }}
            </style>
            <meta http-equiv="refresh" content="3">
        </head>
        <body>
            <h2>🕷️ 去重防污開源爬蟲實驗室</h2>
            
            <div class="container">
                <div class="dish-card" style="border-color: #00ffaa55;">
                    <h3 style="color: #00ffaa; margin: 0 0 10px 0;">🟢 左側：去重育種探針</h3>
                    <div class="petri" style="border-color: #00ffaa44;">
                        <div class="core" style="{p_core}"></div>
                    </div>
                    <div class="info">心跳: #{p['heartbeat']} | 能量: {p['energy']} EP</div>
                    <div class="msg">{p['status']}</div>
                    <a class="btn" style="background: {p_btn_color};" href="/?track=precision&action={p_btn_action}">{p_btn_text}</a>
                </div>

                <div class="dish-card" style="border-color: #00aaff55;">
                    <h3 style="color: #00aaff; margin: 0 0 10px 0;">🔵 右側：野生基因混血</h3>
                    <div class="petri" style="border-color: #00aaff44;">
                        <div class="core" style="{w_core}"></div>
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
    threading.Thread(target=precision_crawler_loop, daemon=True).start()
    threading.Thread(target=wild_crawler_loop, daemon=True).start()
    
    server = HTTPServer(('127.0.0.1', 8080), CrawlerDashboardHandler)
    print("🕷️ 去重防污爬蟲實驗室已啟動！請在瀏覽器打開: http://127.0.0.1:8080")
    server.serve_forever()
