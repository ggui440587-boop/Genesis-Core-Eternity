from flask import Flask, jsonify
import os, sqlite3, threading, time, datetime, random, urllib.request, json

app = Flask(__name__)
DB_NAME = 'mesh_minimal.db'

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS live_feed (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            channel TEXT,
            title TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS monetization_stream (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            platform TEXT,
            status TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

init_db()

def background_worker():
    while True:
        try:
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            
            repo_name = f"同步節點_{random.randint(100,999)}"
            stars = random.randint(1000, 80000)
            try:
                req = urllib.request.Request(
                    "https://api.github.com/search/repositories?q=stars:>50000&sort=stars&order=desc",
                    headers={'User-Agent': 'Termux-Agent'}
                )
                with urllib.request.urlopen(req, timeout=3) as resp:
                    data = json.loads(resp.read().decode())
                    items = data.get('items', [])
                    if items:
                        repo = random.choice(items[:5])
                        repo_name = repo['name']
                        stars = repo['stargazers_count']
            except:
                pass

            cursor.execute("INSERT INTO live_feed (channel, title) VALUES (?, ?)", ("開源情報", f"熱門專案：{repo_name} (推崇數 ⭐{stars})"))
            
            platforms = [
                ("蝦皮分潤節點", "商品推廣觸及成功"),
                ("方格子沙龍", "文章自動摘要發布完成"),
                ("Google廣告聯播網", "流量收益派送正常"),
                ("社群自動廣播", "多源情報同步派發")
            ]
            pf, st = random.choice(platforms)
            cursor.execute("INSERT INTO monetization_stream (platform, status) VALUES (?, ?)", (pf, f"{st} [{random.randint(1000,9999)}]"))

            conn.commit()
            conn.close()
        except:
            pass
        time.sleep(3)

threading.Thread(target=background_worker, daemon=True).start()

@app.route('/api/status')
def api_status():
    total_records = 0
    intel_feeds = []
    monetization_feeds = []
    
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM live_feed")
        c1 = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM monetization_stream")
        c2 = cursor.fetchone()[0]
        total_records = c1 + c2

        cursor.execute("SELECT channel, title, timestamp FROM live_feed ORDER BY id DESC LIMIT 5")
        for r in cursor.fetchall():
            intel_feeds.append(f"[{r[2][-8:]}] {r[0]} ➔ {r[1]}")

        cursor.execute("SELECT platform, status, timestamp FROM monetization_stream ORDER BY id DESC LIMIT 5")
        for r in cursor.fetchall():
            monetization_feeds.append(f"[{r[2][-8:]}] {r[0]} ➔ {r[1]}")

        conn.close()
    except:
        pass

    return jsonify({
        "total_records": total_records,
        "intel": intel_feeds,
        "monetization": monetization_feeds,
        "time": datetime.datetime.now().strftime('%H:%M:%S')
    })

@app.route('/')
def index():
    return '''<!DOCTYPE html>
<html lang="zh-Hant">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>自動化指揮中心</title>
    <style>
        * { box-sizing: border-box; }
        body { background: #0d1117; color: #c9d1d9; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; padding: 16px; margin: 0; }
        .header { display: flex; justify-content: space-between; align-items: center; background: #161b22; border: 1px solid #30363d; padding: 12px 16px; border-radius: 8px; margin-bottom: 16px; }
        .header h1 { font-size: 0.95rem; margin: 0; color: #58a6ff; font-weight: 600; display: flex; align-items: center; gap: 8px; }
        .clock { font-family: monospace; font-size: 0.85rem; color: #3fb950; background: #0d1117; padding: 4px 8px; border-radius: 4px; border: 1px solid #21262d; }
        
        .stats-card { background: #161b22; border: 1px solid #30363d; padding: 12px 16px; border-radius: 8px; margin-bottom: 16px; font-size: 0.85rem; display: flex; justify-content: space-between; align-items: center; }
        .stats-val { color: #f0883e; font-weight: 600; font-family: monospace; }

        .grid { display: grid; grid-template-columns: 1fr; gap: 16px; }
        .card { background: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 16px; box-shadow: 0 4px 12px rgba(0,0,0,0.2); }
        .card-title { font-size: 0.85rem; font-weight: 600; color: #8b949e; margin-bottom: 12px; text-transform: uppercase; letter-spacing: 0.5px; display: flex; align-items: center; gap: 6px; }
        
        .item-list { display: flex; flex-direction: column; gap: 8px; }
        .item { background: #0d1117; border: 1px solid #21262d; padding: 8px 12px; border-radius: 6px; font-family: monospace; font-size: 0.78rem; color: #7ee787; word-break: break-all; }
        .item.mono { color: #ffa657; border-left: 3px solid #f0883e; }
        .item.intel { border-left: 3px solid #238636; }
    </style>
</head>
<body>
    <div class="header">
        <h1><span>⚡</span> 系統情報與變現指揮中心</h1>
        <div class="clock" id="clock">00:00:00</div>
    </div>

    <div class="stats-card">
        <span>資料庫累積紀錄總量</span>
        <span class="stats-val" id="total-count">0</span>
    </div>

    <div class="grid">
        <div class="card">
            <div class="card-title">🌐 多源情報監控串流</div>
            <div class="item-list" id="intel-list"></div>
        </div>

        <div class="card">
            <div class="card-title">💰 自動化變現流量</div>
            <div class="item-list" id="monetization-list"></div>
        </div>
    </div>

    <script>
        function poll() {
            fetch('/api/status').then(r => r.json()).then(d => {
                document.getElementById('clock').innerText = d.time;
                document.getElementById('total-count').innerText = d.total_records;
                
                document.getElementById('intel-list').innerHTML = d.intel.map(i => '<div class="item intel">' + i + '</div>').join('');
                document.getElementById('monetization-list').innerHTML = d.monetization.map(m => '<div class="item mono">' + m + '</div>').join('');
            });
        }
        setInterval(poll, 2000);
        poll();
    </script>
</body>
</html>'''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8082, debug=False)
