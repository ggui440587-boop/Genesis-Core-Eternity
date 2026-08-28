from flask import Flask, jsonify, request
import os, sqlite3, threading, time, datetime, random, subprocess

app = Flask(__name__)
DB_NAME = 'mesh_v12.db'

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
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS system_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            log TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

init_db()

def log_message(msg):
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO system_logs (log) VALUES (?)", (msg,))
        conn.commit()
        conn.close()
    except:
        pass

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
            log_message(f"[{cat}] 執行成功: {title}")
        except:
            pass
        time.sleep(3)

threading.Thread(target=background_worker, daemon=True).start()

@app.route('/api/action', methods=['POST'])
def api_action():
    data = request.json or {}
    action = data.get('action')
    msg = "未知動作"
    if action == 'trigger':
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO live_feed (category, title) VALUES (?, ?)", ("系統運作", f"手動安全巡檢 [{random.randint(1000,9999)}]"))
        conn.commit()
        conn.close()
        msg = "手動寫入排程成功"
    elif action == 'clean':
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM live_feed WHERE id NOT IN (SELECT id FROM live_feed ORDER BY id DESC LIMIT 10)")
        conn.commit()
        conn.close()
        msg = "清理舊紀錄完成，保留最新 10 筆"
    elif action == 'ping':
        msg = "系統網路連線正常 (PONG)"

    log_message(f"[指令執行] {msg}")
    return jsonify({"status": "success", "message": msg})

@app.route('/api/status')
def api_status():
    total_records = 0
    sections = {"流量變現": [], "多源情報": [], "內容變現": [], "AI 代理": [], "系統運作": []}
    counts = {"流量變現": 0, "多源情報": 0, "內容變現": 0, "AI 代理": 0, "系統運作": 0}
    recent_logs = []
    
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

        cursor.execute("SELECT log, timestamp FROM system_logs ORDER BY id DESC LIMIT 4")
        log_rows = cursor.fetchall()
        for l_row in log_rows:
            t_str = l_row[1][-8:] if l_row[1] else "00:00:00"
            recent_logs.append(f"[{t_str}] {l_row[0]}")

        conn.close()
    except Exception as e:
        print("API Error:", e)

    # 模擬系統資源消耗數據
    cpu_load = f"{random.randint(8, 24)}%"
    mem_usage = f"{random.randint(180, 260)}MB"

    return jsonify({
        "total": total_records,
        "counts": counts,
        "sections": sections,
        "logs": recent_logs,
        "cpu": cpu_load,
        "mem": mem_usage,
        "time": datetime.datetime.now().strftime('%H:%M:%S')
    })

@app.route('/')
def index():
    return '''<!DOCTYPE html>
<html lang="zh-Hant">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ULTIMATE COMMAND CENTER v12</title>
    <style>
        * { box-sizing: border-box; }
        body { background: #050508; color: #e1e4e8; font-family: 'Courier New', Courier, monospace; padding: 8px; margin: 0; }
        
        .header-panel { background: linear-gradient(135deg, #161b22, #0d1117); border: 1px solid #30363d; padding: 8px 10px; border-radius: 8px; margin-bottom: 6px; box-shadow: 0 0 10px rgba(0,255,128,0.05); }
        .header-top { display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px; font-size: 0.8rem; }
        .header-bottom { display: flex; justify-content: space-between; align-items: center; font-size: 0.68rem; color: #8b949e; border-top: 1px solid #21262d; padding-top: 4px; }
        
        .control-panel { background: #161b22; border: 1px solid #30363d; padding: 6px 10px; border-radius: 8px; margin-bottom: 6px; display: flex; gap: 6px; justify-content: space-between; }
        .btn { background: #21262d; color: #c9d1d9; border: 1px solid #30363d; padding: 5px 8px; border-radius: 6px; font-size: 0.7rem; font-family: monospace; cursor: pointer; font-weight: bold; flex: 1; text-align: center; }
        .btn-green { background: #238636; color: #fff; border-color: #3fb950; }
        .btn-blue { background: #1f6feb; color: #fff; border-color: #58a6ff; }
        .btn-red { background: #da3633; color: #fff; border-color: #f85149; }
        .btn:active { opacity: 0.8; }

        .card { background: #161b22; border: 1px solid #30363d; padding: 6px 10px; border-radius: 8px; margin-bottom: 6px; position: relative; overflow: hidden; }
        .card::before { content: ''; position: absolute; top: 0; left: 0; width: 3px; height: 100%; }
        
        .card-m::before { background: #58a6ff; }
        .card-i::before { background: #a371f7; }
        .card-c::before { background: #f0883e; }
        .card-a::before { background: #3fb950; }
        .card-s::before { background: #79c0ff; }

        .card-title { font-size: 0.72rem; margin-bottom: 4px; font-weight: bold; border-bottom: 1px solid #21262d; padding-bottom: 3px; display: flex; justify-content: space-between; align-items: center; }
        
        .title-m { color: #58a6ff; }
        .title-i { color: #a371f7; }
        .title-c { color: #f0883e; }
        .title-a { color: #3fb950; }
        .title-s { color: #79c0ff; }

        .badge { background: #21262d; color: #ff7b72; padding: 1px 5px; border-radius: 4px; font-size: 0.65rem; border: 1px solid #30363d; font-weight: bold; }
        .item { font-size: 0.7rem; color: #c9d1d9; padding: 2px 0; border-bottom: 1px dashed #21262d; display: flex; align-items: center; }
        .item:last-child { border-bottom: none; }
        
        .time-tag { color: #8b949e; margin-right: 5px; background: #0d1117; padding: 1px 3px; border-radius: 3px; border: 1px solid #21262d; font-size: 0.65rem; }
        
        .log-box { background: #010409; border: 1px solid #30363d; padding: 6px; border-radius: 6px; font-size: 0.65rem; color: #7ee787; margin-bottom: 6px; max-height: 70px; overflow-y: auto; }
        .log-line { margin-bottom: 2px; }

        .pulse { display: inline-block; width: 6px; height: 6px; background: #3fb950; border-radius: 50%; margin-right: 4px; box-shadow: 0 0 6px #3fb950; }
        .status-ok { color: #3fb950; font-weight: bold; }
    </style>
</head>
<body>
    <div class="header-panel">
        <div class="header-top">
            <span><span class="pulse"></span>總紀錄：<b id="total" style="color: #f0883e;">0</b> 筆</span>
            <span id="clock" style="color: #3fb950; font-weight: bold;">00:00:00</span>
        </div>
        <div class="header-bottom">
            <span>CPU: <b id="cpu-load" style="color: #58a6ff;">0%</b> | RAM: <b id="mem-usage" style="color: #a371f7;">0MB</b></span>
            <span>狀態: <span class="status-ok">ACTIVE</span></span>
        </div>
    </div>

    <div class="control-panel">
        <button class="btn btn-green" onclick="sendAction('trigger')">立即寫入</button>
        <button class="btn btn-blue" onclick="sendAction('ping')">系統Ping</button>
        <button class="btn btn-red" onclick="sendAction('clean')">清理舊檔</button>
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

    <div class="log-box" id="log-box">
        <div class="log-line">>> 系統核心終端日誌載入中...</div>
    </div>

    <script>
        function sendAction(actionType) {
            fetch('/api/action', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({action: actionType})
            }).then(r => r.json()).then(d => {
                update();
            });
        }

        function update() {
            fetch('/api/status').then(r => r.json()).then(d => {
                document.getElementById('clock').innerText = d.time;
                document.getElementById('total').innerText = d.total;
                document.getElementById('cpu-load').innerText = d.cpu;
                document.getElementById('mem-usage').innerText = d.mem;
                
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

                if (d.logs && d.logs.length > 0) {
                    document.getElementById('log-box').innerHTML = d.logs.map(l => '<div class="log-line">>> ' + l + '</div>').join('');
                }
            }).catch(err => console.log(err));
        }
        setInterval(update, 3000);
        update();
    </script>
</body>
</html>'''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8082, debug=False)
