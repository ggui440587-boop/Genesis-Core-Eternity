from flask import Flask, jsonify
import os, sqlite3, threading, time, datetime, random

app = Flask(__name__)
DB_NAME = 'mesh_minimal.db'

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS live_feed (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT,
            title TEXT,
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
            
            # 分類與內容配對
            tasks = [
                ("【變現】", "蝦皮分潤推播成功"),
                ("【變現】", "方格子沙龍文章發布"),
                ("【情報】", "GitHub 熱門專案同步"),
                ("【變現】", "Google 廣告收益更新")
            ]
            cat, title = random.choice(tasks)
            content = f"{title} [{random.randint(1000,9999)}]"
            
            cursor.execute("INSERT INTO live_feed (category, title) VALUES (?, ?)", (cat, content))
            conn.commit()
            conn.close()
        except:
            pass
        time.sleep(3)

threading.Thread(target=background_worker, daemon=True).start()

@app.route('/api/status')
def api_status():
    total_records = 0
    feeds = []
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM live_feed")
        total_records = cursor.fetchone()[0]

        # 維持只顯示最新 3 筆，並加上分類標籤
        cursor.execute("SELECT category, title, timestamp FROM live_feed ORDER BY id DESC LIMIT 3")
        for r in cursor.fetchall():
            feeds.append(f"{r[2][-8:]} {r[0]} {r[1]}")
        conn.close()
    except:
        pass

    return jsonify({
        "total": total_records,
        "feeds": feeds,
        "time": datetime.datetime.now().strftime('%H:%M:%S')
    })

@app.route('/')
def index():
    return '''<!DOCTYPE html>
<html lang="zh-Hant">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>極簡指揮中心</title>
    <style>
        body { background: #0d1117; color: #c9d1d9; font-family: monospace; padding: 12px; margin: 0; }
        .box { background: #161b22; border: 1px solid #30363d; padding: 10px 14px; border-radius: 6px; margin-bottom: 10px; display: flex; justify-content: space-between; font-size: 0.85rem; }
        .card { background: #161b22; border: 1px solid #30363d; padding: 10px 12px; border-radius: 6px; }
        .item { font-size: 0.78rem; color: #7ee787; padding: 5px 0; border-bottom: 1px solid #21262d; }
        .item:last-child { border-bottom: none; }
    </style>
</head>
<body>
    <div class="box">
        <span>總紀錄：<b id="total" style="color: #f0883e;">0</b></span>
        <span id="clock" style="color: #3fb950;">00:00:00</span>
    </div>

    <div class="card">
        <div id="list"></div>
    </div>

    <script>
        function update() {
            fetch('/api/status').then(r => r.json()).then(d => {
                document.getElementById('clock').innerText = d.time;
                document.getElementById('total').innerText = d.total;
                document.getElementById('list').innerHTML = d.feeds.map(f => '<div class="item">' + f + '</div>').join('');
            });
        }
        setInterval(update, 2000);
        update();
    </script>
</body>
</html>'''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8082, debug=False)
