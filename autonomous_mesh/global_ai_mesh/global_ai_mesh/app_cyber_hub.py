from flask import Flask, jsonify, request
import os, sqlite3, threading, time, datetime, random

app = Flask(__name__)
DB_NAME = 'mesh_v11.db'

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
                ("多源情報", "GitHub 熱門專案與 RSS 擴張"),
                ("內容變現", "自動化影片腳本與多平台分發"),
                ("AI 代理", "Model Context Protocol 同步"),
                ("AI 代理", "LLM API 智慧排程與調用"),
                ("系統運作", "Termux 背景行程 nohup 監控"),
                ("系統運作", "記憶體防禦與資料庫備份")
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

@app.route('/api/trigger', methods=['POST'])
def api_trigger():
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO live_feed (category, title) VALUES (?, ?)", ("AI 代理", f"手動觸發模型向量檢索 [{random.randint(1000,9999)}]"))
        conn.commit()
        conn.close()
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route('/api/status')
def api_status():
    total_records = 0
    sections = {"流量變現": [], "多源情報": [], "內容變現": [], "AI 代理": [], "系統運作": []}
    counts = {"流量變現": 0, "多源情報": 0, "內容變現": 0, "AI 代理": 0, "系統運作": 0}
    
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM live_feed")
        res = cursor.fetchone()
        total_records = res[0] if res else 0

        for cat in sections.keys():
            cursor.execute("SELECT COUNT(*) FROM live_feed WHERE category = ?", (cat,))
            c_res = cursor.fetchone()
            counts[cat] = c_res[0] if c_res else 0

            cursor.execute("SELECT title, timestamp FROM live_feed WHERE category = ? ORDER BY id DESC LIMIT 2", (cat,))
            rows = cursor.fetchall()
            feed_list = []
            for row in rows:
                t_str = row[1][-8:] if row[1] else "00:00:00"
                feed_list.append(f"<span class='time-tag'>{t_str}</span> ➔ {row[0]}")
            sections[cat] = feed_list if feed_list else ["等待同步中..."]

        conn.close()
    except Exception as e:
        print("API Error:", e)

    return jsonify({
        "total": total_records,
        "counts": counts,
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
    <title>CYBER COMMAND CENTER v11</title>
    <style>
        * { box-sizing: border-box; }
        body { background: #050508; color: #e1e4e8; font-family: 'Courier New', Courier, monospace; padding: 8px; margin: 0; }
        
        .header-panel { background: linear-gradient(135deg, #161b22, #0d1117); border: 1px solid #30363d; padding: 10px; border-radius: 8px; margin-bottom: 8px; box-shadow: 0 0 10px rgba(0,255,128,0.05); }
        .header-top { display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px; font-size: 0.85rem; }
        .header-bottom { display: flex; justify-content: space-between; align-items: center; font-size: 0.72rem; color: #8b949e; border-top: 1px solid #21262d; padding-top: 5px; }
        
        .control-panel { background: #161b22; border: 1px solid #30363d; padding: 8px 10px; border-radius: 8px; margin-bottom: 8px; display: flex; justify-content: space-between; align-items: center; }
        .btn { background: linear-gradient(135deg, #238636, #2ea043); color: #ffffff; border: 1px solid #3fb950; padding: 5px 12px; border-radius: 6px; font-size: 0.75rem; font-family: monospace; cursor: pointer; font-weight: bold; box-shadow: 0 0 8px rgba(46,160,67,0.4); }
        .btn:active { background: #238636; box-shadow: none; }

        .card { background: #161b22; border: 1px solid #30363d; padding: 8px 10px; border-radius: 8px; margin-bottom: 8px; position: relative; overflow: hidden; }
        .card::before { content: ''; position: absolute; top: 0; left: 0; width: 3px; height: 100%; }
        
        .card-m::before { background: #58a6ff; }
        .card-i::before { background: #a371f7; }
        .card-c::before { background: #f0883e; }
        .card-a::before { background: #3fb950; }
        .card-s::before { background: #79c0ff; }

        .card-title { font-size: 0.75rem; margin-bottom: 5px; font-weight: bold; border-bottom: 1px solid #21262d; padding-bottom: 4px; display: flex; justify-content: space-between; align-items: center; }
        
        .title-m { color: #58a6ff; }
        .title-i { color: #a371f7; }
        .title-c { color: #f0883e; }
        .title-a { color: #3fb950; }
        .title-s { color: #79c0ff; }

        .badge { background: #21262d; color: #ff7b72; padding: 2px 6px; border-radius: 4px; font-size: 0.68rem; border: 1px solid #30363d; font-weight: bold; }
        .item { font-size: 0.72rem; color: #c9d1d9; padding: 3px 0; border-bottom: 1px dashed #21262d; display: flex; align-items: center; }
        .item:last-child { border-bottom: none; }
        
        .time-tag { color: #8b949e; margin-right: 6px; background: #0d1117; padding: 1px 4px; border-radius: 3px; border: 1px solid #21262d; font-size: 0.68rem; }
        
        .pulse { display: inline-block; width: 7px; height: 7px; background: #3fb950; border-radius: 50%; margin-right: 5px; box-shadow: 0 0 8px #3fb950; animation: blink 1.5px infinite; }
        @keyframes blink { 0% { opacity: 1; } 50% { opacity: 0.4; } 100% { opacity: 1; } }
        
        .status-ok { color: #3fb950; font-weight: bold; text-shadow: 0 0 5px rgba(63,185,80,0.3); }
    </style>
</head>
<body>
    <div class="header-panel">
        <div class="header-top">
            <span><span class="pulse"></span>總資料庫紀錄：<b id="total" style="color: #f0883e; font-size: 0.95rem;">0</b> 筆</span>
            <span id="clock" style="color: #3fb950; font-weight: bold;">00:00:00</span>
        </div>
        <div class="header-bottom">
            <span>核心防禦狀態：<span class="status-ok">SECURE / ACTIVE</span></span>
            <span>更新頻率：3秒</span>
        </div>
    </div>

    <div class="control-panel">
        <span style="font-size: 0.72rem; color: #8b949e;">控制項：手動發動一次模擬排程</span>
        <button class="btn" onclick="triggerTask()">立即寫入</button>
    </div>

    <div class="card card-m">
        <div class="card-title title-m">
            <span>🌐 流量變現模組</span>
            <span class="badge" id="cnt-m">0 筆</span>
        </div>
        <div id="sec-m">載入中...</div>
    </div>

    <div class="card card-i">
        <div class="card-title title-i">
            <span>📡 多源情報擴張</span>
            <span class="badge" id="cnt-i">0 筆</span>
        </div>
        <div id="sec-i">載入中...</div>
    </div>

    <div class="card card-c">
        <div class="card-title title-c">
            <span>⚡ 自動化內容變現流</span>
            <span class="badge" id="cnt-c">0 筆</span>
        </div>
        <div id="sec-c">載入中...</div>
    </div>

    <div class="card card-a">
        <div class="card-title title-a">
            <span>🤖 AI 服務與模型代理</span>
            <span class="badge" id="cnt-a">0 筆</span>
        </div>
        <div id="sec-a">載入中...</div>
    </div>

    <div class="card card-s">
        <div class="card-title title-s">
            <span>⚙️ 系統運作核心</span>
            <span class="badge" id="cnt-s">0 筆</span>
        </div>
        <div id="sec-s">載入中...</div>
    </div>

    <script>
        function triggerTask() {
            fetch('/api/trigger', {method: 'POST'}).then(r => r.json()).then(d => {
                update();
            });
        }

        function update() {
            fetch('/api/status').then(r => r.json()).then(d => {
                document.getElementById('clock').innerText = d.time;
                document.getElementById('total').innerText = d.total;
                
                document.getElementById('cnt-m').innerText = (d.counts["流量變現"] || 0) + " 筆";
                document.getElementById('cnt-i').innerText = (d.counts["多源情報"] || 0) + " 筆";
                document.getElementById('cnt-c').innerText = (d.counts["內容變現"] || 0) + " 筆";
                document.getElementById('cnt-a').innerText = (d.counts["AI 代理"] || 0) + " 筆";
                document.getElementById('cnt-s').innerText = (d.counts["系統運作"] || 0) + " 筆";

                document.getElementById('sec-m').innerHTML = (d.sections["流量變現"] || []).map(i => '<div class="item">' + i + '</div>').join('');
                document.getElementById('sec-i').innerHTML = (d.sections["多源情報"] || []).map(i => '<div class="item">' + i + '</div>').join('');
                document.getElementById('sec-c').innerHTML = (d.sections["內容變現"] || []).map(i => '<div class="item">' + i + '</div>').join('');
                document.getElementById('sec-a').innerHTML = (d.sections["AI 代理"] || []).map(i => '<div class="item">' + i + '</div>').join('');
                document.getElementById('sec-s').innerHTML = (d.sections["系統運作"] || []).map(i => '<div class="item">' + i + '</div>').join('');
            }).catch(err => console.log(err));
        }
        setInterval(update, 3000);
        update();
    </script>
</body>
</html>'''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8082, debug=False)
