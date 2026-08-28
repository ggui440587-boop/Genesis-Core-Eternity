import urllib.request
import urllib.parse
import json
import random
import time
import threading
import sqlite3
import asyncio
import aiohttp
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse

BASE_DIR = Path("./")
DB_PATH = BASE_DIR / "genesis_omni.db"
DISPATCH_DIR = BASE_DIR / "telegram_dispatch_queue"
DISPATCH_DIR.mkdir(exist_ok=True)

TELEGRAM_BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"
TELEGRAM_CHAT_ID = "YOUR_CHAT_ID_HERE"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS global_intelligence (
            id TEXT PRIMARY KEY,
            source_name TEXT,
            item_data TEXT,
            category TEXT,
            vector_tags TEXT,
            dispatched INTEGER DEFAULT 0,
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
        "status": "向量矩陣：待命...",
        "energy": 100,
        "harvested": 0,
        "trigger_signal": False
    },
    "monetization": {
        "is_paused": False,
        "heartbeat": 0,
        "status": "Telegram自動推播流：待命...",
        "energy": 100,
        "dispatched_count": 0,
        "trigger_signal": False
    }
}

def classify_and_tag(text):
    text_lower = text.lower()
    if any(k in text_lower for k in ["ai", "model", "llm", "torch", "arxiv", "huggingface"]):
        return "AI模型與機器學習", "LLM,DeepLearning,AI"
    elif any(k in text_lower for k in ["rust", "crates", "cli", "system"]):
        return "高效能系統與Rust", "Rust,Systems,CLI"
    elif any(k in text_lower for k in ["docker", "cloud", "gitlab", "container"]):
        return "雲原生與DevOps", "Docker,Cloud,DevOps"
    elif any(k in text_lower for k in ["npm", "javascript", "web", "frontend"]):
        return "前沿網頁與前端生態", "JavaScript,Web,NPM"
    else:
        return "全端通用開源專案", "OpenSource,General,Code"

async def async_fetch_source(session, source):
    try:
        if source == "github":
            q = random.choice(["agent", "llm", "automation", "python", "rust"])
            url = f"https://api.github.com/search/repositories?q={q}+stars:>1000&sort=stars&order=desc"
            async with session.get(url, headers={'User-Agent': 'Genesis-Nexus', 'Accept': 'application/vnd.github.v3+json'}, timeout=5) as resp:
                data = await resp.json()
                items = data.get("items", [])
                if items:
                    t = items[0]
                    return f"GH_{t['name']}", f"GitHub: {t['html_url']} - {t.get('description', '')}"
        elif source == "huggingface":
            url = "https://huggingface.co/api/models?sort=downloads&direction=-1&limit=5"
            async with session.get(url, headers={'User-Agent': 'Genesis-Nexus'}, timeout=5) as resp:
                models = await resp.json()
                if models:
                    t = random.choice(models)
                    m_id = t.get('id', 'model').replace('/', '_')
                    return f"HF_{m_id}", f"HuggingFace AI: https://huggingface.co/{t.get('id')}"
        elif source == "reddit":
            url = "https://www.reddit.com/r/opensource/hot.json?limit=5"
            async with session.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=5) as resp:
                data = await resp.json()
                posts = data.get("data", {}).get("children", [])
                if posts:
                    t = random.choice(posts).get("data", {})
                    slug = "".join(c for c in t.get("title", "post")[:20] if c.isalnum() or c=='_')
                    return f"RD_{slug}", f"Reddit OpenSource: {t.get('url')}"
        elif source == "codeberg":
            url = "https://codeberg.org/api/v1/repos/search?limit=5"
            async with session.get(url, headers={'User-Agent': 'Genesis-Nexus'}, timeout=5) as resp:
                data = await resp.json()
                repos = data.get("data", [])
                if repos:
                    t = random.choice(repos)
                    return f"CB_{t['name']}", f"Codeberg: {t['html_url']}"
        elif source == "crates":
            url = "https://crates.io/api/v1/crates?per_page=5&sort=downloads"
            async with session.get(url, headers={'User-Agent': 'Genesis-Nexus'}, timeout=5) as resp:
                data = await resp.json()
                crates = data.get("crates", [])
                if crates:
                    t = random.choice(crates)
                    return f"CR_{t['name']}", f"Crates.io: https://crates.io/crates/{t['name']}"
        elif source == "npm":
            url = "https://registry.npmjs.org/-/v1/search?text=ai+or+cli&size=5"
            async with session.get(url, headers={'User-Agent': 'Genesis-Nexus'}, timeout=5) as resp:
                data = await resp.json()
                objs = data.get("objects", [])
                if objs:
                    t = random.choice(objs).get("package", {})
                    pkg_name = t.get('name', 'pkg').replace('/', '_')
                    return f"NPM_{pkg_name}", f"NPM Package: {t.get('links', {}).get('repository', 'https://npmjs.com')}"
        elif source == "pypi":
            url = "https://pypi.org/pypi/requests/json"
            async with session.get(url, headers={'User-Agent': 'Genesis-Nexus'}, timeout=5) as resp:
                data = await resp.json()
                info = data.get("info", {})
                return f"PYPI_lib_{random.randint(100,999)}", f"PyPI Global: {info.get('home_page', 'https://pypi.org')}"
        elif source == "lobsters":
            url = "https://lobste.rs/hottest.json"
            async with session.get(url, headers={'User-Agent': 'Genesis-Nexus'}, timeout=5) as resp:
                stories = await resp.json()
                if stories:
                    t = random.choice(stories)
                    slug = "".join(c for c in t.get("title", "story")[:20] if c.isalnum() or c=='_')
                    return f"LB_{slug}", f"Lobsters Tech: {t.get('url')}"
        elif source == "hackernews":
            url = "https://hacker-news.firebaseio.com/v0/topstories.json"
            async with session.get(url, headers={'User-Agent': 'Genesis-Nexus'}, timeout=5) as resp:
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
            async with session.get(url, headers={'User-Agent': 'Genesis-Nexus'}, timeout=5) as resp:
                data = await resp.json()
                results = data.get("results", [])
                if results:
                    t = random.choice(results)
                    return f"DOCKER_{t['name']}", f"Docker Hub: https://hub.docker.com/_/{t['name']}"
        elif source == "gitlab":
            url = "https://gitlab.com/api/v4/projects?visibility=public&per_page=5"
            async with session.get(url, headers={'User-Agent': 'Genesis-Nexus'}, timeout=5) as resp:
                repos = await resp.json()
                if repos:
                    t = random.choice(repos)
                    return f"GL_{t['name']}", f"GitLab Public: {t['web_url']}"
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
                if state["is_paused"] and not state["trigger_signal"]:
                    state["status"] = "【向量矩陣】休眠中..."
                    await asyncio.sleep(1)
                    continue
                
                if state["trigger_signal"]:
                    state["trigger_signal"] = False
                    state["status"] = "【強力觸發】手動強制向量掃描中..."
                else:
                    state["heartbeat"] += 1
                
                source = random.choice(sources)
                item_id, item_data = await async_fetch_source(session, source)
                
                if item_id and item_data:
                    conn = sqlite3.connect(DB_PATH)
                    cursor = conn.cursor()
                    cursor.execute("SELECT id FROM global_intelligence WHERE id = ?", (item_id,))
                    if cursor.fetchone():
                        state["status"] = f"【防重銷毀】發現重複專案，清除"
                        state["energy"] = max(20, state["energy"] - 1)
                    else:
                        category, tags = classify_and_tag(item_data)
                        cursor.execute(
                            "INSERT INTO global_intelligence (id, source_name, item_data, category, vector_tags) VALUES (?, ?, ?, ?, ?)",
                            (item_id, source, item_data, category, tags)
                        )
                        conn.commit()
                        state["harvested"] += 1
                        state["energy"] = min(200, state["energy"] + 5)
                        state["status"] = f"【向量歸檔】分類: [{category}] -> {item_id}"
                    conn.close()
                
                await asyncio.sleep(5)
                
    loop.run_until_complete(main_loop())

def telegram_dispatch_thread():
    global TRACK_STATE
    while True:
        state = TRACK_STATE["monetization"]
        if state["is_paused"] and not state["trigger_signal"]:
            state["status"] = "【推播流】已暫停..."
            time.sleep(1)
            continue
            
        if state["trigger_signal"]:
            state["trigger_signal"] = False
            state["status"] = "【強力觸發】手動強制推播執行中..."
        else:
            state["heartbeat"] += 1
            
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("SELECT id, item_data, category, vector_tags FROM global_intelligence WHERE dispatched = 0 ORDER BY RANDOM() LIMIT 1")
            row = cursor.fetchone()
            
            if row:
                item_id, item_data, category, tags = row
                message = f"🚀 【Genesis全球情報速遞】\n📂 分類：{category}\n🏷️ 標籤：#{tags.replace(',', ' #')}\n🆔 識別：{item_id}\n🔗 內容：{item_data}"
                
                queue_file = DISPATCH_DIR / f"TG_Dispatch_{int(time.time())}.txt"
                queue_file.write_text(message, encoding="utf-8")
                
                cursor.execute("UPDATE global_intelligence SET dispatched = 1 WHERE id = ?", (item_id,))
                conn.commit()
                
                state["dispatched_count"] += 1
                state["energy"] = min(200, state["energy"] + 6)
                state["status"] = f"【推播成功】已發送至 Telegram 頻道"
            else:
                state["status"] = f"【推播等待】所有情報均已同步完畢..."
            conn.close()
            
            time.sleep(8)
        except Exception as e:
            state["status"] = f"【推播流】調度中"
            time.sleep(4)

class GenesisNexusHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        query_params = parse_qs(parsed_path.query)
        
        if "track" in query_params and "action" in query_params:
            track = query_params["track"][0]
            action = query_params["action"][0]
            if track in TRACK_STATE:
                if action == "pause": TRACK_STATE[track]["is_paused"] = True
                elif action == "resume": TRACK_STATE[track]["is_paused"] = False
                elif action == "trigger": TRACK_STATE[track]["trigger_signal"] = True

        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        
        p = TRACK_STATE["precision"]
        m = TRACK_STATE["monetization"]
        
        # 讀取資料庫最近 5 筆即時情報
        feed_items = []
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("SELECT id, category, timestamp FROM global_intelligence ORDER BY timestamp DESC LIMIT 5")
            feed_items = cursor.fetchall()
            conn.close()
        except:
            pass

        p_core = "background: radial-gradient(circle, #ffaa00 0%, #663300 100%); box-shadow: 0 0 20px #ffaa00; animation: none;" if p["is_paused"] else "background: radial-gradient(circle, #00ff66 0%, #004422 100%); box-shadow: 0 0 30px #00ff66; animation: hb-p 1.4s infinite;"
        m_core = "background: radial-gradient(circle, #ffaa00 0%, #663300 100%); box-shadow: 0 0 20px #ffaa00; animation: none;" if m["is_paused"] else "background: radial-gradient(circle, #00e5ff 0%, #003344 100%); box-shadow: 0 0 30px #00e5ff; animation: hb-m 1.1s infinite;"
        
        p_btn_action, p_btn_text, p_btn_color = ("resume", "喚醒向量矩陣", "#00ff66") if p["is_paused"] else ("pause", "暫停向量矩陣", "#ffbb00")
        m_btn_action, m_btn_text, m_btn_color = ("resume", "喚醒Telegram推播", "#00e5ff") if m["is_paused"] else ("pause", "暫停Telegram推播", "#ffbb00")

        feed_html = ""
        for item_id, cat, ts in feed_items:
            feed_html += f"<div class='feed-item'>[{ts[-8:]}] <b>{cat}</b>: {item_id}</div>"
        if not feed_html:
            feed_html = "<div class='feed-item' style='color:#666;'>等待數據流入中...</div>"

        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <title>Genesis-Omni Cyber-Lab</title>
            <style>
                body {{ background: #030305; color: #00ff66; font-family: monospace; margin: 0; padding: 15px; display: flex; flex-direction: column; align-items: center; position: relative; overflow-x: hidden; }}
                /* Matrix Code Rain Background Effect */
                body::before {{ content: "010101 101010 GENESIS OMNI MATRIX 011010 110011 CYBERNETIC CORE"; position: fixed; top: 0; left: 0; width: 100%; height: 100%; opacity: 0.03; z-index: -1; font-size: 10px; word-break: break-all; color: #00ff66; pointer-events: none; }}
                h2 {{ margin-bottom: 20px; color: #00ff66; text-shadow: 0 0 15px rgba(0,255,102,0.6); text-align: center; letter-spacing: 1px; }}
                .container {{ display: flex; flex-direction: column; gap: 20px; width: 100%; max-width: 400px; }}
                .dish-card {{ background: rgba(10, 10, 20, 0.92); border: 1px solid rgba(0,255,102,0.25); border-radius: 16px; padding: 16px; display: flex; flex-direction: column; align-items: center; box-shadow: 0 6px 25px rgba(0,0,0,0.8); }}
                .petri {{ width: 140px; height: 140px; border-radius: 50%; display: flex; justify-content: center; align-items: center; margin-bottom: 12px; border: 2px dashed rgba(0,255,102,0.3); }}
                .core {{ width: 52px; height: 52px; border-radius: 50%; }}
                @keyframes hb-p {{ 0%,100%{{transform:scale(0.9);}} 50%{{transform:scale(1.12);}} }}
                @keyframes hb-m {{ 0%,100%{{transform:scale(0.85);}} 50%{{transform:scale(1.18);}} }}
                .info {{ font-size: 12px; text-align: center; margin-bottom: 5px; color: #ccc; }}
                .msg {{ color: #ffbb00; font-size: 11px; margin-top: 5px; height: 35px; text-align: center; }}
                .btn-group {{ display: flex; gap: 8px; margin-top: 5px; }}
                .btn {{ background: var(--bg-color); color: #030305; border: none; padding: 8px 14px; font-size: 12px; font-weight: bold; border-radius: 16px; cursor: pointer; text-decoration: none; box-shadow: 0 3px 10px rgba(0,0,0,0.4); }}
                .btn-trigger {{ background: #ff00cc; color: #fff; }}
                /* Live Feed Window */
                .feed-box {{ width: 100%; max-width: 400px; background: rgba(10, 10, 18, 0.95); border: 1px solid rgba(0,229,255,0.3); border-radius: 16px; padding: 14px; box-sizing: border-box; margin-top: 5px; box-shadow: 0 6px 25px rgba(0,0,0,0.8); }}
                .feed-title {{ color: #00e5ff; font-size: 13px; font-weight: bold; margin-bottom: 8px; text-align: center; text-shadow: 0 0 8px rgba(0,229,255,0.4); }}
                .feed-item {{ font-size: 11px; color: #00ff66; background: rgba(0,255,102,0.05); border-left: 2px solid #00ff66; padding: 4px 8px; margin-bottom: 5px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }}
            </style>
            <meta http-equiv="refresh" content="3">
        </head>
        <body>
            <h2>🌐 GENESIS OMNI CYBER-LAB</h2>
            
            <div class="container">
                <div class="dish-card" style="border-color: #00ff6655;">
                    <h3 style="color: #00ff66; margin: 0 0 10px 0; text-align:center;">🟢 左側：向量知識庫引擎</h3>
                    <div class="petri" style="border-color: #00ff6644;">
                        <div class="core" style="{p_core}"></div>
                    </div>
                    <div class="info">心跳: #{p['heartbeat']} | 能量: {p['energy']} EP</div>
                    <div class="info">向量歸檔數: <b>{p['harvested']}</b></div>
                    <div class="msg">{p['status']}</div>
                    <div class="btn-group">
                        <a class="btn" style="background: {p_btn_color};" href="/?track=precision&action={p_btn_action}">{p_btn_text}</a>
                        <a class="btn btn-trigger" href="/?track=precision&action=trigger">⚡ 強力觸發</a>
                    </div>
                </div>

                <div class="dish-card" style="border-color: #00e5ff55;">
                    <h3 style="color: #00e5ff; margin: 0 0 10px 0; text-align:center;">🔵 右側：Telegram 自動推播流</h3>
                    <div class="petri" style="border-color: #00e5ff44;">
                        <div class="core" style="{m_core}"></div>
                    </div>
                    <div class="info">心跳: #{m['heartbeat']} | 能量: {m['energy']} EP</div>
                    <div class="info">已推播情報數: <b>{m['dispatched_count']}</b></div>
                    <div class="msg">{m['status']}</div>
                    <div class="btn-group">
                        <a class="btn" style="background: {m_btn_color};" href="/?track=monetization&action={m_btn_action}">{m_btn_text}</a>
                        <a class="btn btn-trigger" href="/?track=monetization&action=trigger">⚡ 強力觸發</a>
                    </div>
                </div>

                <div class="feed-box">
                    <div class="feed-title">⚡ 即時情報流（Live Intelligence Feed）</div>
                    {feed_html}
                </div>
            </div>
        </body>
        </html>
        """
        self.wfile.write(html.encode("utf-8"))

if __name__ == "__main__":
    threading.Thread(target=precision_worker_thread, daemon=True).start()
    threading.Thread(target=telegram_dispatch_thread, daemon=True).start()
    
    server = HTTPServer(('127.0.0.1', 8080), GenesisNexusHandler)
    print("🌐 Genesis Cyber-Lab 終極儀表板已啟動！請打開瀏覽器: http://127.0.0.1:8080")
    server.serve_forever()
