import urllib.request
import urllib.parse
import json
import random
import time
import threading
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse

BASE_DIR = Path("./")
PRECISION_DIR = BASE_DIR / "ultimate_precision"
WILD_DIR = BASE_DIR / "ultimate_wild"

PRECISION_DIR.mkdir(exist_ok=True)
WILD_DIR.mkdir(exist_ok=True)

# 全域多源狀態
TRACK_STATE = {
    "precision": {
        "is_paused": False,
        "heartbeat": 0,
        "status": "全域情報網：待命...",
        "energy": 100,
        "sources_harvested": 0
    },
    "wild": {
        "is_paused": False,
        "heartbeat": 0,
        "status": "野生混血區：待命...",
        "energy": 100,
        "mutations_born": 0
    }
}

# ==================== 全域多源爬蟲探針 (左側精準育種) ====================
def global_precision_loop():
    global TRACK_STATE
    sources = ["github", "huggingface", "reddit", "codeberg"]
    
    while True:
        state = TRACK_STATE["precision"]
        if state["is_paused"]:
            state["status"] = "【左側】已進入冬眠休眠..."
            time.sleep(1)
            continue
            
        try:
            state["heartbeat"] += 1
            chosen_source = random.choice(sources)
            item_id = None
            item_data = None
            
            # 1. GitHub 探針
            if chosen_source == "github":
                state["status"] = "【全域探針】正在掃描 GitHub 開源專案..."
                query = random.choice(["ai agent", "python automation", "LLM tool", "scraper"])
                url = f"https://api.github.com/search/repositories?q={urllib.request.quote(query)}+language:python&sort=stars&order=desc"
                req = urllib.request.Request(url, headers={'User-Agent': 'Ultimate-Bot', 'Accept': 'application/vnd.github.v3+json'})
                with urllib.request.urlopen(req, timeout=10) as resp:
                    data = json.loads(resp.read().decode('utf-8'))
                    items = data.get("items", [])
                    if items:
                        target = items[0]
                        item_id = f"GH_{target['name']}"
                        item_data = f"GitHub: {target['html_url']}"

            # 2. Hugging Face 探針
            elif chosen_source == "huggingface":
                state["status"] = "【全域探針】正在掃描 Hugging Face AI 模型..."
                url = "https://huggingface.co/api/models?sort=downloads&direction=-1&limit=5"
                req = urllib.request.Request(url, headers={'User-Agent': 'Ultimate-Bot'})
                with urllib.request.urlopen(req, timeout=10) as resp:
                    models = json.loads(resp.read().decode('utf-8'))
                    if models:
                        target = random.choice(models)
                        item_id = f"HF_{target.get('id', 'model').replace('/', '_')}"
                        item_data = f"HuggingFace: https://huggingface.co/{target.get('id')}"

            # 3. Reddit 開源看板探針
            elif chosen_source == "reddit":
                state["status"] = "【全域探針】正在掃描 Reddit 開源熱門板..."
                url = "https://www.reddit.com/r/opensource/hot.json?limit=5"
                req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
                with urllib.request.urlopen(req, timeout=10) as resp:
                    data = json.loads(resp.read().decode('utf-8'))
                    posts = data.get("data", {}).get("children", [])
                    if posts:
                        target = random.choice(posts).get("data", {})
                        title_slug = "".join(c for c in target.get("title", "post")[:30] if c.isalnum() or c=='_')
                        item_id = f"RD_{title_slug}"
                        item_data = f"Reddit: {target.get('url')}"

            # 4. Codeberg 去中心化開源探針
            elif chosen_source == "codeberg":
                state["status"] = "【全域探針】正在掃描 Codeberg 開源庫..."
                url = "https://codeberg.org/api/v1/repos/search?limit=5"
                req = urllib.request.Request(url, headers={'User-Agent': 'Ultimate-Bot'})
                with urllib.request.urlopen(req, timeout=10) as resp:
                    data = json.loads(resp.read().decode('utf-8'))
                    repos = data.get("data", [])
                    if repos:
                        target = random.choice(repos)
                        item_id = f"CB_{target['name']}"
                        item_data = f"Codeberg: {target['html_url']}"

            # 審判與去重銷毀機制
            if item_id and item_data:
                target_file = PRECISION_DIR / f"{item_id}.txt"
                if target_file.exists():
                    state["status"] = f"【防重銷毀】捕獲重複項目，已當場清除"
                    state["energy"] = max(20, state["energy"] - 1)
                else:
                    target_file.write_text(item_data, encoding="utf-8")
                    state["sources_harvested"] += 1
                    state["energy"] = min(150, state["energy"] + 4)
                    state["status"] = f"【左側收編】成功捕獲並歸檔: {item_id}"
            
            time.sleep(8)
        except Exception as e:
            state["status"] = f"【左側】防護罩隔離連線波動"
            time.sleep(4)

# ==================== 野生混血突變區 (右側) ====================
def global_wild_loop():
    global TRACK_STATE
    while True:
        state = TRACK_STATE["wild"]
        if state["is_paused"]:
            state["status"] = "【右側】已進入冬眠休眠..."
            time.sleep(1)
            continue
            
        try:
            state["heartbeat"] += 1
            state["status"] = f"【野生突變】正在進行跨源基因重組..."
            
            chimera_id = f"Chimera_X_{random.randint(10000, 99999)}"
            w_file = WILD_DIR / f"{chimera_id}.txt"
            
            # 80% 突變成功，20% 基因崩潰直接銷毀
            if random.random() < 0.8:
                w_file.write_text(f"Cross-platform mutated organism born at heartbeat #{state['heartbeat']}", encoding="utf-8")
                state["mutations_born"] += 1
                state["energy"] = min(150, state["energy"] + 5)
                state["status"] = f"【右側突變】成功誕生跨界新物種！"
            else:
                if w_file.exists(): w_file.unlink()
                state["energy"] = max(20, state["energy"] - 3)
                state["status"] = f"【右側銷毀】基因排斥，殘骸已徹底清除"
                
            time.sleep(7)
        except Exception as e:
            state["status"] = f"【右側】野生亂流隔離中"
            time.sleep(4)

# ==================== 網頁即時儀表板 ====================
class UltimateDashboardHandler(BaseHTTPRequestHandler):
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
        
        p_core = "background: radial-gradient(circle, #ffaa00 0%, #663300 100%); box-shadow: 0 0 20px #ffaa00; animation: none;" if p["is_paused"] else "background: radial-gradient(circle, #00ffcc 0%, #004466 100%); box-shadow: 0 0 25px #00ffcc; animation: hb-p 1.5s infinite;"
        w_core = "background: radial-gradient(circle, #ffaa00 0%, #663300 100%); box-shadow: 0 0 20px #ffaa00; animation: none;" if w["is_paused"] else "background: radial-gradient(circle, #ff00aa 0%, #660044 100%); box-shadow: 0 0 25px #ff00aa; animation: hb-w 1.2s infinite;"
        
        p_btn_action, p_btn_text, p_btn_color = ("resume", "喚醒全域探針", "#00ffcc") if p["is_paused"] else ("pause", "暫停全域探針", "#ffbb00")
        w_btn_action, w_btn_text, w_btn_color = ("resume", "喚醒野生突變", "#ff00aa") if w["is_paused"] else ("pause", "暫停野生突變", "#ffbb00")

        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <title>Ultimate Multi-Source Bio-Lab</title>
            <style>
                body {{ background: #08080c; color: #fff; font-family: monospace; margin: 0; padding: 15px; display: flex; flex-direction: column; align-items: center; }}
                h2 {{ margin-bottom: 20px; color: #00ffcc; text-shadow: 0 0 10px rgba(0,255,204,0.3); }}
                .container {{ display: flex; flex-direction: column; gap: 20px; width: 100%; max-width: 400px; }}
                .dish-card {{ background: rgba(20, 20, 30, 0.9); border: 1px solid rgba(255,255,255,0.1); border-radius: 14px; padding: 15px; display: flex; flex-direction: column; align-items: center; box-shadow: 0 4px 15px rgba(0,0,0,0.5); }}
                .petri {{ width: 140px; height: 140px; border-radius: 50%; display: flex; justify-content: center; align-items: center; margin-bottom: 12px; border: 2px dashed rgba(255,255,255,0.2); }}
                .core {{ width: 50px; height: 50px; border-radius: 50%; }}
                @keyframes hb-p {{ 0%,100%{{transform:scale(0.9);}} 50%{{transform:scale(1.1);}} }}
                @keyframes hb-w {{ 0%,100%{{transform:scale(0.85);}} 50%{{transform:scale(1.15);}} }}
                .info {{ font-size: 12px; text-align: center; margin-bottom: 5px; }}
                .msg {{ color: #ffbb00; font-size: 11px; margin-top: 5px; height: 30px; text-align: center; }}
                .btn {{ background: var(--bg-color); color: #08080c; border: none; padding: 8px 20px; font-size: 13px; font-weight: bold; border-radius: 20px; cursor: pointer; text-decoration: none; box-shadow: 0 2px 8px rgba(0,0,0,0.3); }}
            </style>
            <meta http-equiv="refresh" content="3">
        </head>
        <body>
            <h2>🌐 全域多源開源實驗室</h2>
            
            <div class="container">
                <div class="dish-card" style="border-color: #00ffcc55;">
                    <h3 style="color: #00ffcc; margin: 0 0 10px 0;">🟢 左側：全域育種 (GH/HF/RD/CB)</h3>
                    <div class="petri" style="border-color: #00ffcc44;">
                        <div class="core" style="{p_core}"></div>
                    </div>
                    <div class="info">心跳: #{p['heartbeat']} | 能量: {p['energy']} EP</div>
                    <div class="info">已收編物種: <b>{p['sources_harvested']}</b></div>
                    <div class="msg">{p['status']}</div>
                    <a class="btn" style="background: {p_btn_color};" href="/?track=precision&action={p_btn_action}">{p_btn_text}</a>
                </div>

                <div class="dish-card" style="border-color: #ff00aa55;">
                    <h3 style="color: #ff00aa; margin: 0 0 10px 0;">🟣 右側：跨界突變區</h3>
                    <div class="petri" style="border-color: #ff00aa44;">
                        <div class="core" style="{w_core}"></div>
                    </div>
                    <div class="info">心跳: #{w['heartbeat']} | 能量: {w['energy']} EP</div>
                    <div class="info">突變成功: <b>{w['mutations_born']}</b></div>
                    <div class="msg">{w['status']}</div>
                    <a class="btn" style="background: {w_btn_color};" href="/?track=wild&action={w_btn_action}">{w_btn_text}</a>
                </div>
            </div>
        </body>
        </html>
        """
        self.wfile.write(html.encode("utf-8"))

if __name__ == "__main__":
    threading.Thread(target=global_precision_loop, daemon=True).start()
    threading.Thread(target=global_wild_loop, daemon=True).start()
    
    server = HTTPServer(('127.0.0.1', 8080), UltimateDashboardHandler)
    print("🌐 全域多源實驗室已啟動！請在瀏覽器打開: http://127.0.0.1:8080")
    server.serve_forever()
