from flask import Flask, jsonify
import os, sqlite3, threading, time, datetime, random

app = Flask(__name__)
DB_NAME = 'mesh_v4.db'

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
            
            categories = [
                ("流量變現", "蝦皮分潤與聯盟推播"),
                ("流量變現", "廣告聯播網收益更新"),
                ("情報同步", "GitHub 熱門開源專案"),
                ("情報同步", "多源情報 RSS 抓取"),
                ("系統運作", "節點心跳與健康檢查"),
                ("系統運作", "自動化排程順利完成")
            ]
            cat, title = random.choice(categories)
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
    sections = {"流量變現": [], "情報同步": [], "系統運作": []}
    
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM live_feed")
        res = cursor.fetchone()
        total_records = res[0] if res else 0

        # 分別抓取各個分類最新的 1 筆
        for cat in sections.keys():
            cursor.execute("SELECT title, timestamp FROM live_feed WHERE category = ? ORDER BY id DESC LIMIT 1", (cat,))
            row = cursor.fetchone()
            if row:
                t_str = row[1][-8:] if row[1] else "00:00:00"
                sections[cat] = f"{t_str} ➔ {row[0]}"
            else:
                sections[cat] = "等待同步中..."

        conn.close()
    except Exception as e:
        print("API Error:", e)

    return jsonify({
        "total": total_records,
        "sections": sections,
        "time": datetime.datetime.now().strftime('%H:%M:%S')
    })

@app.route('/')
def index():
    return '''<!DOCTYPE html>
<html lang="zh-Hant">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>分類指揮中心</title>
    <style>
        body { background: #0d1117; color: #c9d1d9; font-family: monospace; padding: 12px; margin: 0; }
        .box { background: #161b22; border: 1px solid #30363d; padding: 10px 14px; border-radius: 6px; margin-bottom: 10px; display: flex; justify-content: space-between; font-size: 0.85rem; }
        .card { background: #161b22; border: 1px solid #30363d; padding: 10px 12px; border-radius: 6px; margin-bottom: 8px; }
        .card-title { font-size: 0.75rem; color: #8b949e; margin-bottom: 4px; text-transform: uppercase; font-weight: bold; }
        .item { font-size: 0.78rem; color: #7ee787; }
    </style>
</head>
<body>
    <div class="box">
        <span>總紀錄：<b id="total" style="color: #f0883e;">0</b></span>
        <span id="clock" style="color: #3fb950;">00:00:00</span>
    </div>

    <div class="card">
        <div class="card-title">🌐 流量變現</div>
        <div class="item" id="sec-m">載入中...</div>
    </div>

    <div class="card">
        <div class="card-title">📡 情報同步</div>
        <div class="item" id="sec-i">載入中...</div>
    </div>

    <div class="card">
        <div class="card-title">⚙️ 系統運作</div>
        <div class="item" id="sec-s">載入中...</div>
    </div>

    <script>
        function update() {
            fetch('/api/status').then(r => r.json()).then(d => {
                document.getElementById('clock').innerText = d.time;
                document.getElementById('total').innerText = d.total;
                document.getElementById('sec-m').innerText = d.sections["流量變現"] || "無資料";
                document.getElementById('sec-i').innerText = d.sections["情报同步"] || d.sections["情報同步"] || "無資料";
                document.getElementById('sec-s').innerText = d.sections["系統運作"] || "無資料";
            }).catch(err => console.log(err));
        }
        setInterval(update, 2000);
        update();
    </script>
</body>
</html>'''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8082, debug=False)
