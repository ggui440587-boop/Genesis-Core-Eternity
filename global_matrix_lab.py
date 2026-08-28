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
PRECISION_DIR = BASE_DIR / "global_matrix_precision"
WILD_DIR = BASE_DIR / "global_matrix_wild"

PRECISION_DIR.mkdir(exist_ok=True)
WILD_DIR.mkdir(exist_ok=True)

TRACK_STATE = {
    "precision": {
        "is_paused": False,
        "heartbeat": 0,
        "status": "全球14源矩陣：待命...",
        "energy": 100,
        "sources_harvested": 0
    },
    "wild": {
        "is_paused": False,
        "heartbeat": 0,
        "status": "全域超維突變區：待命...",
        "energy": 100,
        "mutations_born": 0
    }
}

# ==================== 全球 14 大頂級情報源矩陣 ====================
def global_matrix_loop():
    global TRACK_STATE
    sources = [
        "github", "huggingface", "reddit", "codeberg", 
        "crates", "npm", "pypi", "lobsters", 
        "hackernews", "arxiv", "dockerhub", "gitlab"
    ]
    
    while True:
        state = TRACK_STATE["precision"]
        if state["is_paused"]:
            state["status"] = "【左側】已進入冬眠休眠..."
            time.sleep(1)
            continue
            
        try:
            state["heartbeat"] += 1
            source = random.choice(sources)
            item_id = None
            item_data = None
            
            # 1. GitHub
            if source == "github":
                state["status"] = "【全球矩陣】掃描 GitHub 頂級開源..."
                q = random.choice(["agent", "llm", "automation", "python", "rust"])
                url = f"https://api.github.com/search/repositories?q={q}+stars:>1000&sort=stars&order=desc"
                req = urllib.request.Request(url, headers={'User-Agent': 'GlobalMatrix-Bot', 'Accept': 'application/vnd.github.v3+json'})
                with urllib.request.urlopen(req, timeout=6) as resp:
                    data = json.loads(resp.read().decode('utf-8'))
                    items = data.get("items", [])
                    if items:
                        t = items[random.randint(0, min(len(items)-1, 4))]
                        item_id = f"GH_{t['name']}"
                        item_data = f"GitHub Global: {t['html_url']}"

            # 2. Hugging Face
            elif source == "huggingface":
                state["status"] = "【全球矩陣】掃描 Hugging Face AI 核心模型..."
                url = "https://huggingface.co/api/models?sort=downloads&direction=-1&limit=10"
                req = urllib.request.Request(url, headers={'User-Agent': 'GlobalMatrix-Bot'})
                with urllib.request.urlopen(req, timeout=6) as resp:
                    models = json.loads(resp.read().decode('utf-8'))
                    if models:
                        t = random.choice(models)
                        m_id = t.get('id', 'model').replace('/', '_')
                        item_id = f"HF_{m_id}"
                        item_data = f"HuggingFace AI: https://huggingface.co/{t.get('id')}"

            # 3. Reddit
            elif source == "reddit":
                state["status"] = "【全球矩陣】掃描 Reddit 開源版..."
                url = "https://www.reddit.com/r/opensource/hot.json?limit=10"
                req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req, timeout=6) as resp:
                    data = json.loads(resp.read().decode('utf-8'))
                    posts = data.get("data", {}).get("children", [])
                    if posts:
                        t = random.choice(posts).get("data", {})
                        slug = "".join(c for c in t.get("title", "post")[:20] if c.isalnum() or c=='_')
                        item_id = f"RD_{slug}"
                        item_data = f"Reddit OpenSource: {t.get('url')}"

            # 4. Codeberg
            elif source == "codeberg":
                state["status"] = "【全球矩陣】掃描 Codeberg 去中心化開源..."
                url = "https://codeberg.org/api/v1/repos/search?limit=10"
                req = urllib.request.Request(url, headers={'User-Agent': 'GlobalMatrix-Bot'})
                with urllib.request.urlopen(req, timeout=6) as resp:
                    data = json.loads(resp.read().decode('utf-8'))
                    repos = data.get("data", [])
                    if repos:
                        t = random.choice(repos)
                        item_id = f"CB_{t['name']}"
                        item_data = f"Codeberg: {t['html_url']}"

            # 5. Crates.io (Rust)
            elif source == "crates":
                state["status"] = "【全球矩陣】掃描 Crates.io (Rust 系統生態)..."
                url = "https://crates.io/api/v1/crates?per_page=10&sort=downloads"
                req = urllib.request.Request(url, headers={'User-Agent': 'GlobalMatrix-Bot'})
                with urllib.request.urlopen(req, timeout=6) as resp:
                    data = json.loads(resp.read().decode('utf-8'))
                    crates = data.get("crates", [])
                    if crates:
                        t = random.choice(crates)
                        item_id = f"CR_{t['name']}"
                        item_data = f"Crates.io: https://crates.io/crates/{t['name']}"

            # 6. npm
            elif source == "npm":
                state["status"] = "【全球矩陣】掃描 npm (全球 JS/TS 模組)..."
                url = "https://registry.npmjs.org/-/v1/search?text=ai+or+cli&size=10"
                req = urllib.request.Request(url, headers={'User-Agent': 'GlobalMatrix-Bot'})
                with urllib.request.urlopen(req, timeout=6) as resp:
                    data = json.loads(resp.read().decode('utf-8'))
                    objs = data.get("objects", [])
                    if objs:
                        t = random.choice(objs).get("package", {})
                        pkg_name = t.get('name', 'pkg').replace('/', '_')
                        item_id = f"NPM_{pkg_name}"
                        item_data = f"NPM Package: {t.get('links', {}).get('repository', 'https://npmjs.com')}"

            # 7. PyPI
            elif source == "pypi":
                state["status"] = "【全球矩陣】掃描 PyPI (Python 頂級庫)..."
                url = "https://pypi.org/pypi/torch/json" # 經典標竿庫範例
                req = urllib.request.Request(url, headers={'User-Agent': 'GlobalMatrix-Bot'})
                with urllib.request.urlopen(req, timeout=6) as resp:
                    data = json.loads(resp.read().decode('utf-8'))
                    info = data.get("info", {})
                    item_id = f"PYPI_global_lib_{random.randint(100,999)}"
                    item_data = f"PyPI Global: {info.get('home_page', 'https://pypi.org')}"

            # 8. Lobsters
            elif source == "lobsters":
                state["status"] = "【全球矩陣】掃描 Lobsters 硬核技術社群..."
                url = "https://lobste.rs/hottest.json"
                req = urllib.request.Request(url, headers={'User-Agent': 'GlobalMatrix-Bot'})
                with urllib.request.urlopen(req, timeout=6) as resp:
                    stories = json.loads(resp.read().decode('utf-8'))
                    if stories:
                        t = random.choice(stories)
                        slug = "".join(c for c in t.get("title", "story")[:20] if c.isalnum() or c=='_')
                        item_id = f"LB_{slug}"
                        item_data = f"Lobsters Tech: {t.get('url')}"

            # 9. Hacker News (YC)
            elif source == "hackernews":
                state["status"] = "【全球矩陣】掃描 Hacker News (全球新創風向)..."
                url = "https://hacker-news.firebaseio.com/v0/topstories.json"
                req = urllib.request.Request(url, headers={'User-Agent': 'GlobalMatrix-Bot'})
                with urllib.request.urlopen(req, timeout=6) as resp:
                    ids = json.loads(resp.read().decode('utf-8'))
                    if ids:
                        top_id = random.choice(ids[:30])
                        item_url = f"https://hacker-news.firebaseio.com/v0/item/{top_id}.json"
                        with urllib.request.urlopen(item_url, timeout=5) as item_resp:
                            item_info = json.loads(item_resp.read().decode('utf-8'))
                            title_slug = "".join(c for c in item_info.get("title", "hn")[:20] if c.isalnum() or c=='_')
                            item_id = f"HN_{top_id}_{title_slug}"
                            item_data = f"HackerNews: {item_info.get('url', 'https://news.ycombinator.com')}"

            # 10. ArXiv API (學術 AI 論文)
            elif source == "arxiv":
                state["status"] = "【全球矩陣】掃描 ArXiv (全球 AI 與電腦科學頂級論文)..."
                url = "http://export.arxiv.org/api/query?search_query=cat:cs.AI&max_results=5"
                req = urllib.request.Request(url, headers={'User-Agent': 'GlobalMatrix-Bot'})
                with urllib.request.urlopen(req, timeout=6) as resp:
                    xml_data = resp.read().decode('utf-8', errors='ignore')
                    import re
                    titles = re.findall(r'<title>(.*?)</title>', xml_data)
                    if len(titles) > 1:
                        t_str = "".join(c for c in titles[random.randint(1, len(titles)-1)][:20] if c.isalnum() or c=='_')
                        item_id = f"ARXIV_{t_str}"
                        item_data = f"ArXiv AI Paper: https://arxiv.org"

            # 11. Docker Hub
            elif source == "dockerhub":
                state["status"] = "【全球矩陣】掃描 Docker Hub 雲原生映像檔..."
                url = "https://hub.docker.com/v2/repositories/library/?page_size=10"
                req = urllib.request.Request(url, headers={'User-Agent': 'GlobalMatrix-Bot'})
                with urllib.request.urlopen(req, timeout=6) as resp:
                    data = json.loads(resp.read().decode('utf-8'))
                    results = data.get("results", [])
                    if results:
                        t = random.choice(results)
                        item_id = f"DOCKER_{t['name']}"
                        item_data = f"Docker Hub Official: https://hub.docker.com/_/{t['name']}"

            # 12. GitLab Public Explore
            elif source == "gitlab":
                state["status"] = "【全球矩陣】掃描 GitLab 公開專案..."
                url = "https://gitlab.com/api/v4/projects?visibility=public&per_page=10"
                req = urllib.request.Request(url, headers={'User-Agent': 'GlobalMatrix-Bot'})
                with urllib.request.urlopen(req, timeout=6) as resp:
                    repos = json.loads(resp.read().decode('utf-8'))
                    if repos:
                        t = random.choice(repos)
                        item_id = f"GL_{t['name']}"
                        item_data = f"GitLab Public: {t['web_url']}"

            # 核心防重、去重與銷毀機制
            if item_id and item_data:
                target_file = PRECISION_DIR / f"{item_id}.txt"
                if target_file.exists():
                    state["status"] = f"【防重銷毀】捕獲全球已知重複專案，當場清除"
                    state["energy"] = max(20, state["energy"] - 1)
                else:
                    target_file.write_text(item_data, encoding="utf-8")
                    state["sources_harvested"] += 1
                    state["energy"] = min(200, state["energy"] + 5)
                    state["status"] = f"【全球收編】成功捕獲頂級世界專案: {item_id}"
            
            time.sleep(6)
        except Exception as e:
            state["status"] = f"【左側】全球高速通道動態調節中"
            time.sleep(4)

# ==================== 全球超維混血突變區 (右側) ====================
def global_matrix_wild_loop():
    global TRACK_STATE
    while True:
        state = TRACK_STATE["wild"]
        if state["is_paused"]:
            state["status"] = "【右側】已進入冬眠休眠..."
            time.sleep(1)
            continue
            
        try:
            state["heartbeat"] += 1
            state["status"] = f"【超維突變】融合全球 14 國技術基因..."
            
            chimera_id = f"Global_Matrix_Node_{random.randint(100000, 999999)}"
            w_file = WILD_DIR / f"{chimera_id}.txt"
            
            if random.random() < 0.82:
                w_file.write_text(f"Global cross-mutated organism born at heartbeat #{state['heartbeat']}", encoding="utf-8")
                state["mutations_born"] += 1
                state["energy"] = min(200, state["energy"] + 6)
                state["status"] = f"【右側突變】誕生全球頂級超維新物種！"
            else:
                if w_file.exists(): w_file.unlink()
                state["energy"] = max(20, state["energy"] - 3)
                state["status"] = f"【右側銷毀】超維基因排斥，殘骸已清除"
                
            time.sleep(5)
        except Exception as e:
            state["status"] = f"【右側】亂流防護中"
            time.sleep(4)

# ==================== 全球儀表板介面 ====================
class MatrixDashboardHandler(BaseHTTPRequestHandler):
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
        
        p_core = "background: radial-gradient(circle, #ffaa00 0%, #663300 100%); box-shadow: 0 0 20px #ffaa00; animation: none;" if p["is_paused"] else "background: radial-gradient(circle, #00ff66 0%, #004422 100%); box-shadow: 0 0 30px #00ff66; animation: hb-p 1.4s infinite;"
        w_core = "background: radial-gradient(circle, #ffaa00 0%, #663300 100%); box-shadow: 0 0 20px #ffaa00; animation: none;" if w["is_paused"] else "background: radial-gradient(circle, #ff00cc 0%, #440033 100%); box-shadow: 0 0 30px #ff00cc; animation: hb-w 1.1s infinite;"
        
        p_btn_action, p_btn_text, p_btn_color = ("resume", "喚醒全球矩陣", "#00ff66") if p["is_paused"] else ("pause", "暫停全球矩陣", "#ffbb00")
        w_btn_action, w_btn_text, w_btn_color = ("resume", "喚醒超維突變", "#ff00cc") if w["is_paused"] else ("pause", "暫停超維突變", "#ffbb00")

        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <title>Global Matrix Bio-Lab</title>
            <style>
                body {{ background: #050508; color: #fff; font-family: monospace; margin: 0; padding: 15px; display: flex; flex-direction: column; align-items: center; }}
                h2 {{ margin-bottom: 20px; color: #00ff66; text-shadow: 0 0 12px rgba(0,255,102,0.4); text-align: center; }}
                .container {{ display: flex; flex-direction: column; gap: 20px; width: 100%; max-width: 400px; }}
                .dish-card {{ background: rgba(15, 15, 25, 0.95); border: 1px solid rgba(255,255,255,0.15); border-radius: 16px; padding: 16px; display: flex; flex-direction: column; align-items: center; box-shadow: 0 6px 20px rgba(0,0,0,0.7); }}
                .petri {{ width: 140px; height: 140px; border-radius: 50%; display: flex; justify-content: center; align-items: center; margin-bottom: 12px; border: 2px dashed rgba(255,255,255,0.25); }}
                .core {{ width: 52px; height: 52px; border-radius: 50%; }}
                @keyframes hb-p {{ 0%,100%{{transform:scale(0.9);}} 50%{{transform:scale(1.12);}} }}
                @keyframes hb-w {{ 0%,100%{{transform:scale(0.85);}} 50%{{transform:scale(1.18);}} }}
                .info {{ font-size: 12px; text-align: center; margin-bottom: 5px; }}
                .msg {{ color: #ffbb00; font-size: 11px; margin-top: 5px; height: 35px; text-align: center; }}
                .btn {{ background: var(--bg-color); color: #050508; border: none; padding: 9px 22px; font-size: 13px; font-weight: bold; border-radius: 20px; cursor: pointer; text-decoration: none; box-shadow: 0 3px 10px rgba(0,0,0,0.4); }}
            </style>
            <meta http-equiv="refresh" content="3">
        </head>
        <body>
            <h2>🌍 全球全景星系開源實驗室</h2>
            
            <div class="container">
                <div class="dish-card" style="border-color: #00ff6655;">
                    <h3 style="color: #00ff66; margin: 0 0 10px 0; text-align:center;">🟢 左側：全球 14 大源矩陣</h3>
                    <div class="petri" style="border-color: #00ff6644;">
                        <div class="core" style="{p_core}"></div>
                    </div>
                    <div class="info">心跳: #{p['heartbeat']} | 能量: {p['energy']} EP</div>
                    <div class="info">全球收編物種: <b>{p['sources_harvested']}</b></div>
                    <div class="msg">{p['status']}</div>
                    <a class="btn" style="background: {p_btn_color};" href="/?track=precision&action={p_btn_action}">{p_btn_text}</a>
                </div>

                <div class="dish-card" style="border-color: #ff00cc55;">
                    <h3 style="color: #ff00cc; margin: 0 0 10px 0; text-align:center;">🟣 右側：超維基因突變</h3>
                    <div class="petri" style="border-color: #ff00cc44;">
                        <div class="core" style="{w_core}"></div>
                    </div>
                    <div class="info">心跳: #{w['heartbeat']} | 能量: {w['energy']} EP</div>
                    <div class="info">超維突變成功: <b>{w['mutations_born']}</b></div>
                    <div class="msg">{w['status']}</div>
                    <a class="btn" style="background: {w_btn_color};" href="/?track=wild&action={w_btn_action}">{w_btn_text}</a>
                </div>
            </div>
        </body>
        </html>
        """
        self.wfile.write(html.encode("utf-8"))

if __name__ == "__main__":
    threading.Thread(target=global_matrix_loop, daemon=True).start()
    threading.Thread(target=global_matrix_wild_loop, daemon=True).start()
    
    server = HTTPServer(('127.0.0.1', 8080), MatrixDashboardHandler)
    print("🌍 全球全景星系實驗室已啟動！請在瀏覽器打開: http://127.0.0.1:8080")
    server.serve_forever()
