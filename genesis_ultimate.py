import urllib.request
import urllib.parse
import json
import random
import time
import threading
import sqlite3
import asyncio
import aiohttp
import re
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse

BASE_DIR = Path("./")
DB_PATH = BASE_DIR / "genesis_hub.db"
MONETIZATION_DIR = BASE_DIR / "automation_monetization"
MONETIZATION_DIR.mkdir(exist_ok=True)

# 初始化 SQLite 資料庫
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS intelligence_hub (
            id TEXT PRIMARY KEY,
            source_name TEXT,
            item_data TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

init_db()

TRACK_STATE = {
    "precision": {
        "is_paused": False,
        "heartbeat": 0,
        "status": "非同步14源矩陣：待命...",
        "energy": 100,
        "sources_harvested": 0
    },
    "monetization": {
        "is_paused": False,
        "heartbeat": 0,
        "status": "自動化內容變現流：待命...",
        "energy": 100,
        "articles_generated": 0
    }
}

# ==================== 非同步 14 大全球情報源與資料庫去重引擎 ====================
async def async_fetch_source(session, source):
    try:
        if source == "github":
            q = random.choice(["agent", "llm", "automation", "python", "rust"])
            url = f"https://api.github.com/search/repositories?q={q}+stars:>1000&sort=stars&order=desc"
            async with session.get(url, headers={'User-Agent': 'Genesis-Ultimate', 'Accept': 'application/vnd.github.v3+json'}, timeout=5) as resp:
                data = await resp.json()
                items = data.get("items", [])
                if items:
                    t = items[0]
                    return f"GH_{t['name']}", f"GitHub: {t['html_url']}"

        elif source == "huggingface":
            url = "https://huggingface.co/api/models?sort=downloads&direction=-1&limit=5"
            async with session.get(url, headers={'User-Agent': 'Genesis-Ultimate'}, timeout=5) as resp:
                models = await resp.json()
                if models:
                    t = random.choice(models)
                    m_id = t.get('id', 'model').replace('/', '_')
                    return f"HF_{m_id}", f"HuggingFace: https://huggingface.co/{t.get('id')}"

        elif source == "reddit":
            url = "https://www.reddit.com/r/opensource/hot.json?limit=5"
            async with session.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=5) as resp:
                data = await resp.json()
                posts = data.get("data", {}).get("children", [])
                if posts:
                    t = random.choice(posts).get("data", {})
                    slug = "".join(c for c in t.get("title", "post")[:20] if c.isalnum() or c=='_')
                    return f"RD_{slug}", f"Reddit: {t.get('url')}"

        elif source == "codeberg":
            url = "https://codeberg.org/api/v1/repos/search?limit=5"
            async with session.get(url, headers={'User-Agent': 'Genesis-Ultimate'}, timeout=5) as resp:
                data = await resp.json()
                repos = data.get("data", [])
                if repos:
                    t = random.choice(repos)
                    return f"CB_{t['name']}", f"Codeberg: {t['html_url']}"

        elif source == "crates":
            url = "https://crates.io/api/v1/crates?per_page=5&sort=downloads"
            async with session.get(url, headers={'User-Agent': 'Genesis-Ultimate'}, timeout=5) as resp:
                data = await resp.json()
                crates = data.get("crates", [])
                if crates:
                    t = random.choice(crates)
                    return f"CR_{t['name']}", f"Crates.io: https://crates.io/crates/{t['name']}"

        elif source == "npm":
            url = "https://registry.npmjs.org/-/v1/search?text=ai+or+cli&size=5"
            async with session.get(url, headers={'User-Agent': 'Genesis-Ultimate'}, timeout=5) as resp:
                data = await resp.json()
                objs = data.get("objects", [])
                if objs:
                    t = random.choice(objs).get("package", {})
                    pkg_name = t.get('name', 'pkg').replace('/', '_')
                    return f"NPM_{pkg_name}", f"NPM: {t.get('links', {}).get('repository', 'https://npmjs.com')}"

        elif source == "pypi":
            url = "https://pypi.org/pypi/requests/json"
            async with session.get(url, headers={'User-Agent': 'Genesis-Ultimate'}, timeout=5) as resp:
                data = await resp.json()
                info = data.get("info", {})
                return f"PYPI_lib_{random.randint(100,999)}", f"PyPI: {info.get('home_page', 'https://pypi.org')}"

        elif source == "lobsters":
            url = "https://lobste.rs/hottest.json"
            async with session.get(url, headers={'User-Agent': 'Genesis-Ultimate'}, timeout=5) as resp:
                stories = await resp.json()
                if stories:
                    t = random.choice(stories)
                    slug = "".join(c for c in t.get("title", "story")[:20] if c.isalnum() or c=='_')
                    return f"LB_{slug}", f"Lobsters: {t.get('url')}"

        elif source == "hackernews":
            url = "https://hacker-news.firebaseio.com/v0/topstories.json"
            async with session.get(url, headers={'User-Agent': 'Genesis-Ultimate'}, timeout=5) as resp:
                ids = await resp.json()
                if ids:
                    top_id = random.choice(ids[:20])
                    item_url = f"https://hacker-news.firebaseio.com/v0/item/{top_id}.json"
                    async with session.get(item_url, timeout=4) as item_resp:
                        item_info = await item_resp.json()
                        slug = "".join(c for c in item_info.get("title", "hn")[:20] if c.isalnum() or c=='_')
                        return f"HN_{top_id}_{slug}", f"HackerNews: {item_info.get('url', 'https://news.ycombinator.com')}"

        elif source == "dockerhub":
            url = "https://hub.docker.com/v2/repositories/library/?page_size=5"
            async with session.get(url, headers={'User-Agent': 'Genesis-Ultimate'}, timeout=5) as resp:
                data = await resp.json()
                results = data.get("results", [])
                if results:
                    t = random.choice(results)
                    return f"DOCKER_{t['name']}", f"DockerHub: https://hub.docker.com/_/{t['name']}"

        elif source == "gitlab":
            url = "https://gitlab.com/api/v4/projects?visibility=public&per_page=5"
            async with session.get(url, headers={'User-Agent': 'Genesis-Ultimate'}, timeout=5) as resp:
                repos = await resp.json()
                if repos:
                    t = random.choice(repos)
                    return f"GL_{t['name']}", f"GitLab: {t['web_url']}"
    except Exception:
        pass
    return None, None

def precision_worker_thread():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    async def main_loop():
        global TRACK_STATE
        sources = ["github", "huggingface", "reddit", "codeberg", "crates", "npm", "pypi", "lobsters", "hackernews", "dockerhub", "gitlab"]
        
        async with aiohttp.ClientSession() as session:
            while True:
                state = TRACK_STATE["precision"]
                if state["is_paused"]:
                    state["status"] = "【左側】非同步矩陣休眠中..."
                    await asyncio.sleep(1)
                    continue
                
                state["heartbeat"] += 1
                source = random.choice(sources)
                state["status"] = f"【非同步探針】正在穿透 {source.upper()} 生態..."
                
                item_id, item_data = await async_fetch_source(session, source)
                
                if item_id and item_data:
                    # 透過 SQLite 資料庫進行極速防重檢查
                    conn = sqlite3.connect(DB_PATH)
                    cursor = conn.cursor()
                    cursor.execute("SELECT id FROM intelligence_hub WHERE id = ?", (item_id,))
                    exists = cursor.fetchone()
                    
                    if exists:
                        state["status"] = f"【資料庫防重】發現重複專案，原地銷毀"
                        state["energy"] = max(20, state["energy"] - 1)
                    else:
                        cursor.execute("INSERT INTO intelligence_hub (id, source_name, item_data) VALUES (?, ?, ?)", (item_id, source, item_data))
                        conn.commit()
                        state["sources_harvested"] += 1
                        state["energy"] = min(200, state["energy"] + 5)
                        state["status"] = f"【入庫收編】成功寫入資料庫: {item_id}"
                    conn.close()
                
                await asyncio.sleep(5)
                
    loop.run_until_complete(main_loop())

# ==================== 自動化內容變現與分發流 (右側) ====================
def monetization_worker_thread():
    global TRACK_STATE
    while True:
        state = TRACK_STATE["monetization"]
        if state["is_paused"]:
            state["status"] = "【右側】變現流已暫停..."
            time.sleep(1)
            continue
            
        try:
            state["heartbeat"] += 1
            state["status"] = "【變現流】正在從資料庫萃取情報並生成變現文案..."
            
            # 從 SQLite 資料庫隨機挑選最新情報來自動化包裝成內容變現摘要
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("SELECT id, item_data FROM intelligence_hub ORDER BY RANDOM() LIMIT 1")
            row = cursor.fetchone()
            conn.close()
            
            if row:
                item_id, item_data = row
                article_content = f"🔥 【全網最新爆款技術速遞】\n專案識別: {item_id}\n來源位址: {item_data}\n自動化分析：本專案具備高度市場潛力與變現應用價值。\n"
                
                file_name = MONETIZATION_DIR / f"Monetize_{int(time.time())}.txt"
                file_name.write_text(article_content, encoding="utf-8")
                
                state["articles_generated"] += 1
                state["energy"] = min(200, state["energy"] + 6)
                state["status"] = f"【變現成功】已產出自動化內容包: {file_name.name}"
            else:
                state["status"] = f"【變現等待】資料庫尚無足夠原料..."
                
            time.sleep(8)
        except Exception as e:
            state["status"] = f"【右側】變現流調節中"
            time.sleep(4)

# ==================== 網頁儀表板控制器 ====================
class GenesisDashboardHandler(BaseHTTPRequestHandler):
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
        m = TRACK_STATE["monetization"]
        
        p_core = "background: radial-gradient(circle, #ffaa00 0%, #663300 100%); box-shadow: 0 0 20px #ffaa00; animation: none;" if p["is_paused"] else "background: radial-gradient(circle, #00ff66 0%, #004422 100%); box-shadow: 0 0 30px #00ff66; animation: hb-p 1.4s infinite;"
        m_core = "background: radial-gradient(circle, #ffaa00 0%, #663300 100%); box-shadow: 0 0 20px #ffaa00; animation: none;" if m["is_paused"] else "background: radial-gradient(circle, #00ccff 0%, #002244 100%); box-shadow: 0 0 30px #00ccff; animation: hb-m 1.1s infinite;"
        
        p_btn_action, p_btn_text, p_btn_color = ("resume", "喚醒非同步矩陣", "#00ff66") if p["is_paused"] else ("pause", "暫停非同步矩陣", "#ffbb00")
        m_btn_action, m_btn_text, m_btn_color = ("resume", "喚醒變現流", "#00ccff") if m["is_paused"] else ("pause", "暫停變現流", "#ffbb00")

        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <title>Genesis-Core Ultimate Dashboard</title>
            <style>
                body {{ background: #050508; color: #fff; font-family: monospace; margin: 0; padding: 15px; display: flex; flex-direction: column; align-items: center; }}
                h2 {{ margin-bottom: 20px; color: #00ff66; text-shadow: 0 0 12px rgba(0,255,102,0.4); text-align: center; }}
                .container {{ display: flex; flex-direction: column; gap: 20px; width: 100%; max-width: 400px; }}
                .dish-card {{ background: rgba(15, 15, 25, 0.95); border: 1px solid rgba(255,255,255,0.15); border-radius: 16px; padding: 16px; display: flex; flex-direction: column; align-items: center; box-shadow: 0 6px 20px rgba(0,0,0,0.7); }}
                .petri {{ width: 140px; height: 140px; border-radius: 50%; display: flex; justify-content: center; align-items: center; margin-bottom: 12px; border: 2px dashed rgba(255,255,255,0.25); }}
                .core {{ width: 52px; height: 52px; border-radius: 50%; }}
                @keyframes hb-p {{ 0%,100%{{transform:scale(0.9);}} 50%{{transform:scale(1.12);}} }}
                @keyframes hb-m {{ 0%,100%{{transform:scale(0.85);}} 50%{{transform:scale(1.18);}} }}
                .info {{ font-size: 12px; text-align: center; margin-bottom: 5px; }}
                .msg {{ color: #ffbb00; font-size: 11px; margin-top: 5px; height: 35px; text-align: center; }}
                .btn {{ background: var(--bg-color); color: #050508; border: none; padding: 9px 22px; font-size: 13px; font-weight: bold; border-radius: 20px; cursor: pointer; text-decoration: none; box-shadow: 0 3px 10px rgba(0,0,0,0.4); }}
            </style>
            <meta http-equiv="refresh" content="3">
        </head>
        <body>
            <h2>⚡ Genesis 終極資料庫與變現中樞</h2>
            
            <div class="container">
                <div class="dish-card" style="border-color: #00ff6655;">
                    <h3 style="color: #00ff66; margin: 0 0 10px 0; text-align:center;">🟢 左側：Asyncio 14源資料庫</h3>
                    <div class="petri" style="border-color: #00ff6644;">
                        <div class="core" style="{p_core}"></div>
                    </div>
                    <div class="info">心跳: #{p['heartbeat']} | 能量: {p['energy']} EP</div>
                    <div class="info">資料庫入庫數: <b>{p['sources_harvested']}</b></div>
                    <div class="msg">{p['status']}</div>
                    <a class="btn" style="background: {p_btn_color};" href="/?track=precision&action={p_btn_action}">{p_btn_text}</a>
                </div>

                <div class="dish-card" style="border-color: #00ccff55;">
                    <h3 style="color: #00ccff; margin: 0 0 10px 0; text-align:center;">🔵 右側：內容變現與分發流</h3>
                    <div class="petri" style="border-color: #00ccff44;">
                        <div class="core" style="{m_core}"></div>
                    </div>
                    <div class="info">心跳: #{m['heartbeat']} | 能量: {m['energy']} EP</div>
                    <div class="info">產出變現包: <b>{m['articles_generated']}</b></div>
                    <div class="msg">{m['status']}</div>
                    <a class="btn" style="background: {m_btn_color};" href="/?track=monetization&action={m_btn_action}">{m_btn_text}</a>
                </div>
            </div>
        </body>
        </html>
        """
        self.wfile.write(html.encode("utf-8"))

if __name__ == "__main__":
    threading.Thread(target=precision_worker_thread, daemon=True).start()
    threading.Thread(target=monetization_worker_thread, daemon=True).start()
    
    server = HTTPServer(('127.0.0.1', 8080), GenesisDashboardHandler)
    print("⚡ Genesis 終極中樞已啟動！請在瀏覽器打開: http://127.0.0.1:8080")
    server.serve_forever()
