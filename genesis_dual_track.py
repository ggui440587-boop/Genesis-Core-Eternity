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
DB_PATH = BASE_DIR / "genesis_dual.db"
BREED_DIR = BASE_DIR / "evolution_specimens"

# 建立分類資料夾
PURE_DIR = BREED_DIR / "同種純化演化"
HYBRID_DIR = BREED_DIR / "全域混合神獸"
PURE_DIR.mkdir(parents=True, exist_ok=True)
HYBRID_DIR.mkdir(parents=True, exist_ok=True)

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS dual_pool (
            id TEXT PRIMARY KEY,
            track_type TEXT,
            category TEXT,
            source_info TEXT,
            generation INTEGER DEFAULT 1,
            score INTEGER DEFAULT 100,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

init_db()

LAB_STATE = {
    "pure": {
        "heartbeat": 100,
        "count": 0,
        "status": "🧬 [同種軌道] 槽位運作中...",
        "peak": "尚無"
    },
    "hybrid": {
        "heartbeat": 100,
        "count": 0,
        "status": "⚡ [混合軌道] 槽位運作中...",
        "peak": "尚無"
    },
    "is_paused": False,
    "trigger_signal": False
}

def classify_category(text):
    text_lower = text.lower()
    if any(k in text_lower for k in ["ai", "model", "llm", "huggingface"]):
        return "AI模型與機器學習"
    elif any(k in text_lower for k in ["rust", "crates"]):
        return "高效能系統與Rust"
    elif any(k in text_lower for k in ["docker", "container"]):
        return "雲原生與DevOps"
    elif any(k in text_lower for k in ["npm", "web", "cli"]):
        return "前沿網頁與前端"
    else:
        return "全端通用開源專案"

async def fetch_seed(session, source):
    try:
        if source == "github":
            url = "https://api.github.com/search/repositories?q=ai+or+rust+stars:>1000&sort=stars"
            async with session.get(url, headers={'User-Agent': 'DualLab'}, timeout=4) as resp:
                data = await resp.json()
                items = data.get("items", [])
                if items:
                    t = random.choice(items)
                    return f"GH_{t['name']}", f"GitHub: {t['html_url']}"
        elif source == "huggingface":
            url = "https://huggingface.co/api/models?limit=5"
            async with session.get(url, headers={'User-Agent': 'DualLab'}, timeout=4) as resp:
                models = await resp.json()
                if models:
                    t = random.choice(models)
                    return f"HF_{t.get('id', 'model').replace('/', '_')}", f"HuggingFace: {t.get('id')}"
        elif source == "crates":
            url = "https://crates.io/api/v1/crates?per_page=5"
            async with session.get(url, headers={'User-Agent': 'DualLab'}, timeout=4) as resp:
                data = await resp.json()
                crates = data.get("crates", [])
                if crates:
                    t = random.choice(crates)
                    return f"CR_{t['name']}", f"Crates.io: {t['name']}"
    except Exception:
        pass
    return f"SEED_{random.randint(100,999)}", "Fallback Seed"

def pure_track_worker():
    """ 同種類型：代代與同類最好的交織演化 """
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    async def worker():
        sources = ["github", "huggingface", "crates"]
        async with aiohttp.ClientSession() as session:
            while True:
                if LAB_STATE["is_paused"] and not LAB_STATE["trigger_signal"]:
                    await asyncio.sleep(1)
                    continue
                
                LAB_STATE["pure"]["heartbeat"] += 1
                source = random.choice(sources)
                seed_id, seed_data = await fetch_seed(session, source)
                cat = classify_category(seed_data)
                
                conn = sqlite3.connect(DB_PATH)
                cursor = conn.cursor()
                
                # 找出同類別中分數最高的前輩進行交織
                cursor.execute("SELECT id, generation, score FROM dual_pool WHERE track_type='pure' AND category=? ORDER BY score DESC LIMIT 1", (cat,))
                ancestor = cursor.fetchone()
                
                if ancestor:
                    anc_id, gen, anc_score = ancestor
                    new_gen = gen + 1
                    new_score = anc_score + random.randint(10, 40)
                    specimen_id = f"PURE_{cat[:2]}_G{new_gen}_{random.randint(100,999)}"
                    info = f"【同種純化】基於前代[{anc_id}]進化"
                else:
                    new_gen = 1
                    new_score = random.randint(100, 200)
                    specimen_id = f"PURE_{cat[:2]}_{random.randint(100,999)}"
                    info = f"【同種初始】源自 {seed_data}"
                
                cursor.execute(
                    "INSERT OR REPLACE INTO dual_pool (id, track_type, category, source_info, generation, score) VALUES (?, 'pure', ?, ?, ?, ?)",
                    (specimen_id, cat, info, new_gen, new_score)
                )
                
                # 同種分類歸檔：建立屬於該類別的資料夾
                sub_dir = PURE_DIR / cat
                sub_dir.mkdir(exist_ok=True)
                with open(sub_dir / f"{specimen_id}.txt", "w", encoding="utf-8") as f:
                    f.write(f"Pure Specimen: {specimen_id}\nCategory: {cat}\nGeneration: {new_gen}\nScore: {new_score}\nInfo: {info}\n")
                
                cursor.execute("SELECT id, score FROM dual_pool WHERE track_type='pure' ORDER BY score DESC LIMIT 1")
                top = cursor.fetchone()
                if top:
                    LAB_STATE["pure"]["peak"] = f"{top[0]} (戰力:{top[1]})"
                
                conn.commit()
                conn.close()
                
                LAB_STATE["pure"]["count"] += 1
                LAB_STATE["pure"]["status"] = f"🟢 同種純化成功: [{cat}] {specimen_id}"
                await asyncio.sleep(5)
                
    loop.run_until_complete(worker())

def hybrid_track_worker():
    """ 混合軌道：跨界融合，全部統一歸納在一個混合資料夾 """
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    async def worker():
        sources = ["github", "huggingface", "crates"]
        async with aiohttp.ClientSession() as session:
            while True:
                if LAB_STATE["is_paused"] and not LAB_STATE["trigger_signal"]:
                    await asyncio.sleep(1)
                    continue
                
                LAB_STATE["hybrid"]["heartbeat"] += 1
                s1 = await fetch_seed(session, random.choice(sources))
                s2 = await fetch_seed(session, random.choice(sources))
                
                conn = sqlite3.connect(DB_PATH)
                cursor = conn.cursor()
                
                # 尋找當前混合池最強的紀錄來進行融合
                cursor.execute("SELECT id, score FROM dual_pool WHERE track_type='hybrid' ORDER BY score DESC LIMIT 1")
                best_hybrid = cursor.fetchone()
                
                if best_hybrid:
                    b_id, b_score = best_hybrid
                    new_score = b_score + random.randint(20, 60)
                    info = f"【混合神獸】融合最強[{b_id}]與異源[{s1[0]}]"
                else:
                    new_score = random.randint(200, 350)
                    info = f"【混合初始】融合 [{s1[0]}] 與 [{s2[0]}]"
                
                specimen_id = f"HYBRID_OMEGA_{random.randint(1000, 9999)}"
                
                cursor.execute(
                    "INSERT OR REPLACE INTO dual_pool (id, track_type, category, source_info, generation, score) VALUES (?, 'hybrid', '全域混合', ?, 99, ?)",
                    (specimen_id, info, new_score)
                )
                
                # 混合軌道產出：統一放入專屬的混合資料夾中
                with open(HYBRID_DIR / f"{specimen_id}.txt", "w", encoding="utf-8") as f:
                    f.write(f"Hybrid Specimen: {specimen_id}\nScore: {new_score}\nParents: {s1[0]} + {s2[0]}\nInfo: {info}\n")
                
                cursor.execute("SELECT id, score FROM dual_pool WHERE track_type='hybrid' ORDER BY score DESC LIMIT 1")
                top = cursor.fetchone()
                if top:
                    LAB_STATE["hybrid"]["peak"] = f"{top[0]} (戰力:{top[1]})"
                
                conn.commit()
                conn.close()
                
                LAB_STATE["hybrid"]["count"] += 1
                LAB_STATE["hybrid"]["status"] = f"⚡ 混合神獸產出: {specimen_id}"
                await asyncio.sleep(6)
                
    loop.run_until_complete(worker())

class DualHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        query_params = parse_qs(parsed_path.query)
        
        if "action" in query_params:
            action = query_params["action"][0]
            if action == "pause": LAB_STATE["is_paused"] = True
            elif action == "resume": LAB_STATE["is_paused"] = False
            elif action == "trigger": LAB_STATE["trigger_signal"] = True

        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        
        p = LAB_STATE["pure"]
        h = LAB_STATE["hybrid"]
        
        # 讀取資料庫顯示狀態
        items_html = ""
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("SELECT id, track_type, category, score FROM dual_pool ORDER BY score DESC LIMIT 8")
            rows = cursor.fetchall()
            for r_id, t_type, cat, score in rows:
                tag = "🟢同種" if t_type == "pure" else "⚡混合"
                items_html += f"<div class='item'>[{tag}] <b>{r_id}</b> ({cat}) | <b>分數:{score}</b></div>"
            conn.close()
        except:
            pass

        if not items_html:
            items_html = "<div class='item'>雙軌演化資料初始化中...</div>"

        btn_text = "暫停雙軌" if not LAB_STATE["is_paused"] else "啟動雙軌"
        btn_act = "pause" if not LAB_STATE["is_paused"] else "resume"

        html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Genesis Dual-Track Lab</title>
    <style>
        body {{ background: #030308; color: #00ff66; font-family: monospace; margin: 0; padding: 12px; display: flex; flex-direction: column; align-items: center; }}
        h2 {{ color: #00ff66; text-align: center; font-size: 16px; }}
        .card {{ background: rgba(10, 15, 25, 0.95); border: 1px solid rgba(0,255,102,0.3); border-radius: 12px; padding: 12px; width: 100%; max-width: 380px; box-sizing: border-box; margin-bottom: 10px; }}
        .info {{ font-size: 11px; color: #ccc; margin-bottom: 4px; }}
        .status {{ font-size: 11px; color: #ffbb00; margin-top: 4px; }}
        .btn {{ background: #00ff66; color: #030308; border: none; padding: 6px 12px; font-weight: bold; border-radius: 8px; cursor: pointer; text-decoration: none; display: inline-block; margin-top: 5px; }}
        .list-box {{ width: 100%; max-width: 380px; background: rgba(10, 15, 25, 0.95); border: 1px solid rgba(255,0,204,0.3); border-radius: 12px; padding: 12px; box-sizing: border-box; }}
        .item {{ font-size: 10px; color: #fff; background: rgba(255,255,255,0.03); border-left: 2px solid #00ff66; padding: 4px 6px; margin-bottom: 4px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }}
    </style>
    <meta http-equiv="refresh" content="3">
</head>
<body>
    <h2>🧬 雙軌演化與產出分類實驗室</h2>
    <div class="card">
        <div class="info"><b>🟢 同種純化軌道</b> (產出數: {p['count']})</div>
        <div class="info">當前同種最強: {p['peak']}</div>
        <div class="status">{p['status']}</div>
    </div>
    <div class="card" style="border-color: rgba(255,0,204,0.4);">
        <div class="info" style="color:#ff00cc;"><b>⚡ 混合融合軌道</b> (產出數: {h['count']})</div>
        <div class="info">當前混合最強: {h['peak']}</div>
        <div class="status" style="color:#00e5ff;">{h['status']}</div>
        <a class="btn" style="background:#ff00cc; color:#fff;" href="/?action={btn_act}">{btn_text}</a>
    </div>
    <div class="list-box">
        <div style="color:#ff00cc; font-size:12px; font-weight:bold; margin-bottom:6px;">🏆 雙軌產出戰力總榜</div>
        {items_html}
    </div>
</body>
</html>"""
        self.wfile.write(html.encode("utf-8"))

if __name__ == "__main__":
    threading.Thread(target=pure_track_worker, daemon=True).start()
    threading.Thread(target=hybrid_track_worker, daemon=True).start()
    
    server = HTTPServer(('127.0.0.1', 8080), DualHandler)
    print("🧬 雙軌演化實驗室已啟動！請在瀏覽器打開: http://127.0.0.1:8080")
    server.serve_forever()
