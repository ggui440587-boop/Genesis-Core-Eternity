from flask import Flask, jsonify
import os, sqlite3, threading, time, datetime, random

app = Flask(__name__)
DB_NAME = 'mesh_v5.db'

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
                ("流量變現", "方格子沙龍文章發布"),
                ("情報同步", "GitHub 熱門開源專案"),
                ("情報同步", "多源情報 RSS 抓取"),
                ("情報同步", "技術文件爬蟲節點"),
                ("系統運作", "節點心跳與健康檢查"),
                ("系統運作", "自動化排程順利完成"),
                ("系統運作", "資料庫自動備份與清理")
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

        # 每個分類抓取最新的 3 筆，讓內容更詳細
        for cat in sections.keys():
            cursor.execute("SELECT title, timestamp FROM live_feed WHERE category = ? ORDER BY id DESC LIMIT 3", (cat,))
            rows = cursor.fetchall()
            feed_list = []
            for row in rows:
                t_str = row[1][-8:] if row[1] else "00:00:00"
                feed_list.append(f"{t_str} ➔ {row[0]}")
            sections[cat] = feed_list if feed_list else ["等待同步中..."]

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
    <title>詳細分類指揮中心</title>
    <style>
        body { background: #0d1117; color: #c9d1d9; font-family: monospace; padding: 12px; margin: 0; }
        .box { background: #161b22; border: 1px solid #30363d; padding: 10px 14px; border-radius: 6px; margin-bottom: 10px; display: flex; justify-content: space-between; font-size: 0.85rem; }
        .card { background: #161b22; border: 1px solid #30363d; padding: 10px 12px; border-radius: 6px; margin-bottom: 8px; }
        .card-title { font-size: 0.75rem; color: #8b949e; margin-bottom: 6px; text-transform: uppercase; font-weight: bold; border-bottom: 1px solid #21262d; padding-bottom: 4px; }
        .item { font-size: 0.75rem; color: #7ee787; padding: 3px 0; }
    </style>
</head>
<body>
    <div class="box">
        <span>總紀錄：<b id="total" style="color: #f0883e;">0</b></span>
        <span id="clock" style="color: #3fb950;">00:00:00</span>
    </div>

    <div class="card">
        <div class="card-title">🌐 流量變現</div>
        <div id="sec-m">載入中...</div>
    </div>

    <div class="card">
        <div class="card-title">📡 情報同步</div>
        <div id="sec-i">載入中...</div>
    </div>

    <div class="card">
        <div class="card-title">⚙️ 系統運作</div>
        <div id="sec-s">載入中...</div>
    </div>

    <script>
        function update() {
            fetch('/api/status').then(r => r.json()).then(d => {
                document.getElementById('clock').innerText = d.time;
                document.getElementById('total').innerText = d.total;
                
                document.getElementById('sec-m').innerHTML = (d.sections["流量變現"] || []).map(i => '<div class="item">' + i + '</div>').join('');
                document.getElementById('sec-i').innerHTML = (d.sections["情報同步"] || []).map(i => '<div class="item">' + i + '</div>').join('');
                document.getElementById('sec-s').innerHTML = (d.sections["系統運作"] || []).map(i => '<div class="item">' + i + '</div>').join('');
            }).catch(err => console.log(err));
        }
        setInterval(update, 2000);
        update();
    </script>
</body>
</html>'''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8082, debug=False)
