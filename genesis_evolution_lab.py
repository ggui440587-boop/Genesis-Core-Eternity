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
DB_PATH = BASE_DIR / "genesis_evolution.db"
BREED_DIR = BASE_DIR / "evolution_specimens"
BREED_DIR.mkdir(exist_ok=True)

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS biological_pool (
            id TEXT PRIMARY KEY,
            track_type TEXT,
            source_name TEXT,
            item_data TEXT,
            category TEXT,
            generation INTEGER DEFAULT 1,
            intelligence INTEGER DEFAULT 50,
            stability INTEGER DEFAULT 50,
            energy_hp INTEGER DEFAULT 100,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

init_db()

TRACK_STATE = {
    "pure": {
        "is_paused": False,
        "heartbeat": 0,
        "status": "左側【同種純化演化】：待命...",
        "total_energy": 100,
        "pure_offspring": 0,
        "trigger_signal": False
    },
    "hybrid": {
        "is_paused": False,
        "heartbeat": 0,
        "status": "右側【跨界突變混血】：待命...",
        "total_energy": 100,
        "hybrid_mutations": 0,
        "trigger_signal": False
    }
}

def classify_category(text):
    text_lower = text.lower()
    if any(k in text_lower for k in ["ai", "model", "llm", "torch", "arxiv", "huggingface"]):
        return "AI模型與機器學習"
    elif any(k in text_lower for k in ["rust", "crates", "cli", "system"]):
        return "高效能系統與Rust"
    elif any(k in text_lower for k in ["docker", "cloud", "gitlab", "container"]):
        return "雲原生與DevOps"
    elif any(k in text_lower for k in ["npm", "javascript", "web", "frontend"]):
        return "前沿網頁與前端生態"
    else:
        return "全端通用開源專案"

async def async_fetch_source(session, source):
    try:
        if source == "github":
            q = random.choice(["agent", "llm", "automation", "python", "rust"])
            url = f"https://api.github.com/search/repositories?q={q}+stars:>1000&sort=stars&order=desc"
            async with session.get(url, headers={'User-Agent': 'EvolutionLab', 'Accept': 'application/vnd.github.v3+json'}, timeout=5) as resp:
                data = await resp.json()
                items = data.get("items", [])
                if items:
                    t = items[0]
                    return f"GH_{t['name']}", f"GitHub: {t['html_url']}"
        elif source == "huggingface":
            url = "https://huggingface.co/api/models?sort=downloads&direction=-1&limit=5"
            async with session.get(url, headers={'User-Agent': 'EvolutionLab'}, timeout=5) as resp:
                models = await resp.json()
                if models:
                    t = random.choice(models)
                    m_id = t.get('id', 'model').replace('/', '_')
                    return f"HF_{m_id}", f"HuggingFace: https://huggingface.co/{t.get('id')}"
        elif source == "crates":
            url = "https://crates.io/api/v1/crates?per_page=5&sort=downloads"
            async with session.get(url, headers={'User-Agent': 'EvolutionLab'}, timeout=5) as resp:
                data = await resp.json()
                crates = data.get("crates", [])
                if crates:
                    t = random.choice(crates)
                    return f"CR_{t['name']}", f"Crates.io: https://crates.io/crates/{t['name']}"
        elif source == "dockerhub":
            url = "https://hub.docker.com/v2/repositories/library/?page_size=5"
            async with session.get(url, headers={'User-Agent': 'EvolutionLab'}, timeout=5) as resp:
                data = await resp.json()
                results = data.get("results", [])
                if results:
                    t = random.choice(results)
                    return f"DOCKER_{t['name']}", f"DockerHub: https://hub.docker.com/_/{t['name']}"
        elif source == "npm":
            url = "https://registry.npmjs.org/-/v1/search?text=ai+or+cli&size=5"
            async with session.get(url, headers={'User-Agent': 'EvolutionLab'}, timeout=5) as resp:
                data = await resp.json()
                objs = data.get("objects", [])
                if objs:
                    t = random.choice(objs).get("package", {})
                    pkg_name = t.get('name', 'pkg').replace('/', '_')
                    return f"NPM_{pkg_name}", f"NPM: {t.get('links', {}).get('repository', 'https://npmjs.com')}"
    except Exception:
        pass
    return None, None

# ==================== 左側：同種純化演化引擎（含數值遺傳） ====================
def pure_breeding_worker():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    async def main_loop():
        global TRACK_STATE
        sources = ["github", "huggingface", "crates", "dockerhub", "npm"]
        
        async with aiohttp.ClientSession() as session:
            while True:
                state = TRACK_STATE["pure"]
                if state["is_paused"] and not state["trigger_signal"]:
                    state["status"] = "左側【同種純化】：休眠中..."
                    await asyncio.sleep(1)
                    continue
                
                if state["trigger_signal"]:
                    state["trigger_signal"] = False
                    state["status"] = "左側【強力觸發】：強制進行同種基因純化..."
                else:
                    state["heartbeat"] += 1
                
                source = random.choice(sources)
                item_id, item_data = await async_fetch_source(session, source)
                
                if item_id and item_data:
                    cat = classify_category(item_data)
                    conn = sqlite3.connect(DB_PATH)
                    cursor = conn.cursor()
                    
                    cursor.execute("SELECT id, intelligence, stability, generation FROM biological_pool WHERE track_type='pure' AND category = ? ORDER BY RANDOM() LIMIT 1", (cat,))
                    ancestor = cursor.fetchone()
                    
                    if ancestor:
                        anc_id, anc_intel, anc_stab, gen = ancestor
                        new_gen = gen + 1
                        new_intel = min(100, int((anc_intel + random.randint(5, 20)) * 1.05))
                        new_stab = min(100, int((anc_stab + random.randint(2, 15)) * 1.02))
                        hp = 120 + (new_gen * 10)
                        
                        offspring_id = f"PURE_{cat[:3]}_G{new_gen}_{random.randint(100,999)}"
                        offspring_data = f"【純血二代物種】祖先[{anc_id}] ⨉ 智力:{new_intel} 穩定:{new_stab}"
                        
                        cursor.execute(
                            "INSERT OR REPLACE INTO biological_pool (id, track_type, source_name, item_data, category, generation, intelligence, stability, energy_hp) VALUES (?, 'pure', ?, ?, ?, ?, ?, ?, ?)",
                            (offspring_id, source, offspring_data, cat, new_gen, new_intel, new_stab, hp)
                        )
                        conn.commit()
                        state["pure_offspring"] += 1
                        state["status"] = f"🟢 成功育出純血物種: {offspring_id} (智:{new_intel})"
                    else:
                        intel = random.randint(40, 70)
                        stab = random.randint(40, 70)
                        cursor.execute(
                            "INSERT OR IGNORE INTO biological_pool (id, track_type, source_name, item_data, category, generation, intelligence, stability, energy_hp) VALUES (?, 'pure', ?, ?, ?, 1, ?, ?, 100)",
                            (item_id, source, item_data, cat, intel, stab)
                        )
                        conn.commit()
                        state["status"] = f"🟢 植入純種母體: {item_id}"
                    conn.close()
                
                await asyncio.sleep(6)
                
    loop.run_until_complete(main_loop())

# ==================== 右側：跨界混血合成引擎（含基因突變與天擇淘汰） ====================
def hybrid_mutant_worker():
    global TRACK_STATE
    while True:
        state = TRACK_STATE["hybrid"]
        if state["is_paused"] and not state["trigger_signal"]:
            state["status"] = "右側【跨界混血】：休眠中..."
            time.sleep(1)
            continue
            
        if state["trigger_signal"]:
            state["trigger_signal"] = False
            state["status"] = "右側【強力觸發】：強制進行跨界突變混血..."
        else:
            state["heartbeat"] += 1
            
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            
            # 天擇淘汰機制：自動清理生命值（HP）歸零或過低的淘汰弱者
            cursor.execute("UPDATE biological_pool SET energy_hp = energy_hp - 15")
            cursor.execute("DELETE FROM biological_pool WHERE energy_hp <= 0")
            conn.commit()
            
            # 撈取兩個不同分類的物種進行突變交配
            cursor.execute("SELECT id, category, intelligence, stability FROM biological_pool ORDER BY RANDOM() LIMIT 2")
            parents = cursor.fetchall()
            
            if len(parents) >= 2:
                p1_id, p1_cat, p1_i, p1_s = parents[0]
                p2_id, p2_cat, p2_i, p2_s = parents[1]
                
                if p1_cat == p2_cat:
                    p2_cat = "跨界特異基因"
                
                hybrid_id = f"MUTANT_{random.randint(1000, 9999)}"
                hybrid_cat = f"混血合成種({p1_cat[:3]}+{p2_cat[:3]})"
                
                # 基因突變演算法：混血會產生爆發性的智力或穩定度成長
                mut_intel = min(100, int((p1_i + p2_i) / 2 + random.randint(15, 35)))
                mut_stab = max(10, int((p1_s + p2_s) / 2 + random.randint(-10, 20)))
                hybrid_data = f"【超級混血突變種】融合[{p1_id}]與[{p2_id}] | 突變智力:{mut_intel} 穩定度:{mut_stab}"
                
                cursor.execute(
                    "INSERT OR REPLACE INTO biological_pool (id, track_type, source_name, item_data, category, generation, intelligence, stability, energy_hp) VALUES (?, 'hybrid', 'mutation_lab', ?, ?, 99, ?, ?, 180)",
                    (hybrid_id, hybrid_data, hybrid_cat, mut_intel, mut_stab)
                )
                conn.commit()
                
                mut_file = BREED_DIR / f"{hybrid_id}.txt"
                mut_file.write_text(hybrid_data, encoding="utf-8")
                
                state["hybrid_mutations"] += 1
                state["status"] = f"🟣 成功孵化混血合成種: {hybrid_id} (智:{mut_intel})"
            else:
                state["status"] = "🟣 基因庫樣本不足，等待育種原料..."
            conn.close()
            
            time.sleep(8)
        except Exception as e:
            state["status"] = "🟣 基因重組與天擇計算中..."
            time.sleep(4)

# ==================== 演化儀表板介面 ====================
class EvolutionHandler(BaseHTTPRequestHandler):
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
        
        p = TRACK_STATE["pure"]
        h = TRACK_STATE["hybrid"]
        
        feed_items = []
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("SELECT id, track_type, category, intelligence, stability, energy_hp FROM biological_pool ORDER BY timestamp DESC LIMIT 6")
            feed_items = cursor.fetchall()
            conn.close()
        except:
            pass

        p_core = "background: radial-gradient(circle, #ffaa00 0%, #663300 100%); box-shadow: 0 0 20px #ffaa00; animation: none;" if p["is_paused"] else "background: radial-gradient(circle, #00ff66 0%, #004422 100%); box-shadow: 0 0 30px #00ff66; animation: hb-p 1.4s infinite;"
        h_core = "background: radial-gradient(circle, #ffaa00 0%, #663300 100%); box-shadow: 0 0 20px #ffaa00; animation: none;" if h["is_paused"] else "background: radial-gradient(circle, #ff00cc 0%, #440033 100%); box-shadow: 0 0 30px #ff00cc; animation: hb-h 1.1s infinite;"
        
        p_btn_action, p_btn_text, p_btn_color = ("resume", "喚醒純化槽", "#00ff66") if p["is_paused"] else ("pause", "暫停純化槽", "#ffbb00")
        h_btn_action, h_btn_text, h_btn_color = ("resume", "喚醒混血槽", "#ff00cc") if h["is_paused"] else ("pause", "暫停混血槽", "#ffbb00")

        feed_html = ""
        for item_id, t_type, cat, intel, stab, hp in feed_items:
            badge_color = "#00ff66" if t_type == "pure" else "#ff00cc"
            badge_text = "【純血】" if t_type == "pure" else "【混血】"
            feed_html += f"<div class='feed-item' style='border-left-color:{badge_color};'><span style='color:{badge_color};'>{badge_text}</span> <b>{item_id}</b> | 智:{intel} 穩:{stab} HP:{hp}</div>"
        if not feed_html:
            feed_html = "<div class='feed-item' style='color:#666;'>物種演化中...</div>"

        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <title>Genesis Specie Evolution Lab</title>
            <style>
                body {{ background: #030305; color: #00ff66; font-family: monospace; margin: 0; padding: 15px; display: flex; flex-direction: column; align-items: center; position: relative; overflow-x: hidden; }}
                body::before {{ content: "GENESIS EVOLUTION LAB NATURAL SELECTION GENETIC MUTATION"; position: fixed; top: 0; left: 0; width: 100%; height: 100%; opacity: 0.03; z-index: -1; font-size: 10px; word-break: break-all; color: #00ff66; pointer-events: none; }}
                h2 {{ margin-bottom: 20px; color: #00ff66; text-shadow: 0 0 15px rgba(0,255,102,0.6); text-align: center; letter-spacing: 1px; }}
                .container {{ display: flex; flex-direction: column; gap: 20px; width: 100%; max-width: 400px; }}
                .dish-card {{ background: rgba(10, 10, 20, 0.92); border: 1px solid rgba(0,255,102,0.25); border-radius: 16px; padding: 16px; display: flex; flex-direction: column; align-items: center; box-shadow: 0 6px 25px rgba(0,0,0,0.8); }}
                .petri {{ width: 140px; height: 140px; border-radius: 50%; display: flex; justify-content: center; align-items: center; margin-bottom: 12px; border: 2px dashed rgba(255,255,255,0.25); }}
                .core {{ width: 52px; height: 52px; border-radius: 50%; }}
                @keyframes hb-p {{ 0%,100%{{transform:scale(0.9);}} 50%{{transform:scale(1.12);}} }}
                @keyframes hb-h {{ 0%,100%{{transform:scale(0.85);}} 50%{{transform:scale(1.18);}} }}
                .info {{ font-size: 12px; text-align: center; margin-bottom: 5px; color: #ccc; }}
                .msg {{ color: #ffbb00; font-size: 11px; margin-top: 5px; height: 35px; text-align: center; }}
                .btn-group {{ display: flex; gap: 8px; margin-top: 5px; }}
                .btn {{ background: var(--bg-color); color: #030305; border: none; padding: 8px 14px; font-size: 12px; font-weight: bold; border-radius: 16px; cursor: pointer; text-decoration: none; box-shadow: 0 3px 10px rgba(0,0,0,0.4); }}
                .btn-trigger {{ background: #00e5ff; color: #030305; }}
                .feed-box {{ width: 100%; max-width: 400px; background: rgba(10, 10, 18, 0.95); border: 1px solid rgba(255,0,204,0.3); border-radius: 16px; padding: 14px; box-sizing: border-box; margin-top: 5px; box-shadow: 0 6px 25px rgba(0,0,0,0.8); }}
                .feed-title {{ color: #ff00cc; font-size: 13px; font-weight: bold; margin-bottom: 8px; text-align: center; text-shadow: 0 0 8px rgba(255,0,204,0.4); }}
                .feed-item {{ font-size: 11px; color: #fff; background: rgba(255,255,255,0.03); border-left: 2px solid #fff; padding: 4px 8px; margin-bottom: 5px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }}
            </style>
            <meta http-equiv="refresh" content="3">
        </head>
        <body>
            <h2>🧬 物種育種與天擇實驗室</h2>
            
            <div class="container">
                <!-- 左側：同種純化演化槽 -->
                <div class="dish-card" style="border-color: #00ff6655;">
                    <h3 style="color: #00ff66; margin: 0 0 10px 0; text-align:center;">🟢 左側：純化演化槽</h3>
                    <div class="petri" style="border-color: #00ff6644;">
                        <div class="core" style="{p_core}"></div>
                    </div>
                    <div class="info">心跳: #{p['heartbeat']} | 純血誕生: <b>{p['pure_offspring']}</b></div>
                    <div class="msg">{p['status']}</div>
                    <div class="btn-group">
                        <a class="btn" style="background: {p_btn_color};" href="/?track=pure&action={p_btn_action}">{p_btn_text}</a>
                        <a class="btn btn-trigger" href="/?track=pure&action=trigger">⚡ 強力純化</a>
                    </div>
                </div>

                <!-- 右側：跨界突變混血槽 -->
                <div class="dish-card" style="border-color: #ff00cc55;">
                    <h3 style="color: #ff00cc; margin: 0 0 10px 0; text-align:center;">🟣 右側：跨界突變混血槽</h3>
                    <div class="petri" style="border-color: #ff00cc44;">
                        <div class="core" style="{h_core}"></div>
                    </div>
                    <div class="info">心跳: #{h['heartbeat']} | 混血誕生: <b>{h['hybrid_mutations']}</b></div>
                    <div class="msg">{h['status']}</div>
                    <div class="btn-group">
                        <a class="btn" style="background: {h_btn_color};" href="/?track=hybrid&action={h_btn_action}">{h_btn_text}</a>
                        <a class="btn btn-trigger" href="/?track=hybrid&action=trigger">⚡ 強力突變</a>
                    </div>
                </div>

                <!-- 物種即時天擇譜系 -->
                <div class="feed-box">
                    <div class="feed-title">🧬 戰力物種譜系與天擇動態</div>
                    {feed_html}
                </div>
            </div>
        </body>
        </html>
        """
        self.wfile.write(html.encode("utf-8"))

if __name__ == "__main__":
    threading.Thread(target=pure_breeding_worker, daemon=True).start()
    threading.Thread(target=hybrid_mutant_worker, daemon=True).start()
    
    server = HTTPServer(('127.0.0.1', 8080), EvolutionHandler)
    print("🧬 演化天擇實驗室已啟動！請在瀏覽器打開: http://127.0.0.1:8080")
    server.serve_forever()
