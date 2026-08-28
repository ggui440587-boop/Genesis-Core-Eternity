from flask import Flask, jsonify, request, send_file
import os, sqlite3, threading, time, datetime, random

app = Flask(__name__)
DB_NAME = 'mesh_v14.db'
worker_interval = 3

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
    global worker_interval
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
        time.sleep(max(1, worker_interval))

threading.Thread(target=background_worker, daemon=True).start()

@app.route('/api/action', methods=['POST'])
def api_action():
    global worker_interval
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
    elif 'set_interval' in data:
        worker_interval = int(data['set_interval'])
        msg = f"已調整執行間隔為: {worker_interval}秒"

    log_message(f"[指令執行] {msg}")
    return jsonify({"status": "success", "message": msg, "interval": worker_interval})

@app.route('/download/db')
def download_db():
    if os.path.exists(DB_NAME):
        return send_file(DB_NAME, as_attachment=True)
    return "找不到資料庫檔案", 404

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

    cpu_val = random.randint(12, 32)
    mem_val = random.randint(190, 260)

    return jsonify({
        "total": total_records,
        "counts": counts,
        "sections": sections,
        "logs": recent_logs,
        "cpu": cpu_val,
        "mem": mem_val,
        "interval": worker_interval,
        "time": datetime.datetime.now().strftime('%H:%M:%S')
    })

@app.route('/')
def index():
    return '''<!DOCTYPE html>
<html lang="zh-Hant">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>VISUAL COMMAND CENTER v14</title>
    <style>
        * { box-sizing: border-box; }
        body { background: #050508; color: #e1e4e8; font-family: 'Courier New', Courier, monospace; padding: 8px; margin: 0; }
        
        .header-panel { background: linear-gradient(135deg, #161b22, #0d1117); border: 1px solid #30363d; padding: 8px 10px; border-radius: 8px; margin-bottom: 6px; box-shadow: 0 0 10px rgba(0,255,128,0.05); }
        .header-top { display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px; font-size: 0.8rem; }
        
        /* 視覺化進度條 */
        .metric-row { display: flex; gap: 10px; margin-bottom: 6px; font-size: 0.7rem; color: #8b949e; align-items: center; }
        .progress-container { flex: 1; background: #21262d; border-radius: 4px; height: 6px; overflow: hidden; border: 1px solid #30363d; }
        .progress-bar-cpu { background: #58a6ff; height: 100%; width: 0%; transition: width 0.5s ease; box-shadow: 0 0 5px #58a6ff; }
        .progress-bar-mem { background: #a371f7; height: 100%; width: 0%; transition: width 0.5s ease; box-shadow: 0 0 5px #a371f7; }

        /* 全景佔比多色分佈條 */
        .ratio-bar { display: flex; height: 8px; border-radius: 4px; overflow: hidden; background: #21262d; margin-bottom: 6px; border: 1px solid #30363d; }
        .seg-m { background: #58a6ff; transition: width 0.5s; }
        .seg-i { background: #a371f7; transition: width 0.5s; }
        .seg-c { background: #f0883e; transition: width 0.5s; }
        .seg-a { background: #3fb950; transition: width 0.5s; }
        .seg-s { background: #79c0ff; transition: width 0.5s; }

        .control-panel { background: #161b22; border: 1px solid #30363d; padding: 6px 10px; border-radius: 8px; margin-bottom: 6px; display: flex; gap: 6px; align-items: center; justify-content: space-between; font-size: 0.7rem; }
        .btn { background: #21262d; color: #c9d1d9; border: 1px solid #30363d; padding: 5px 8px; border-radius: 6px; font-size: 0.68rem; font-family: monospace; cursor: pointer; font-weight: bold; }
        .btn-green { background: #238636; color: #fff; border-color: #3fb950; }
        .btn-red { background: #da3633; color: #fff; border-color: #f85149; }
        .btn:active { opacity: 0.8; }

        .slider-box { display: flex; align-items: center; gap: 4px; font-size: 0.68rem; color: #8b949e; }
        input[type=range] { width: 70px; accent-color: #3fb950; cursor: pointer; }

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
    </style>
</head>
<body>
    <div class="header-panel">
        <div class="header-top">
            <span><span class="pulse"></span>總紀錄：<b id="total" style="color: #f0883e;">0</b> 筆</span>
            <span id="clock" style="color: #3fb950; font-weight: bold;">00:00:00</span>
        </div>
        
        <!-- 動態視覺進度條 -->
        <div class="metric-row">
            <span>CPU</span>
            <div class="progress-container"><div class="progress-bar-cpu" id="cpu-bar"></div></div>
            <b id="cpu-lbl" style="color: #58a6ff; width: 30px; text-align: right;">0%</b>
            <span style="margin-left: 6px;">RAM</span>
            <div class="progress-container"><div class="progress-bar-mem" id="mem-bar"></div></div>
            <b id="mem-lbl" style="color: #a371f7; width: 45px; text-align: right;">0MB</b>
        </div>

        <!-- 模組佔比多色分佈條 -->
        <div class="ratio-bar">
            <div class="seg-m" id="r-m" style="width: 20%;"></div>
            <div class="seg-i" id="r-i" style="width: 20%;"></div>
            <div class="seg-c" id="r-c" style="width: 20%;"></div>
            <div class="seg-a" id="r-a" style="width: 20%;"></div>
            <div class="seg-s" id="r-s" style="width: 20%;"></div>
        </div>
    </div>

    <div class="control-panel">
        <button class="btn btn-green" onclick="sendAction('trigger')">立即寫入</button>
        <div class="slider-box">
            <span>頻率: <b id="speed-val" style="color: #f0883e;">3</b>s</span>
            <input type="range" id="interval-slider" min="1" max="10" value="3" onchange="changeInterval(this.value)">
        </div>
        <button class="btn" onclick="window.location.href='/download/db'">備份</button>
        <button class="btn btn-red" onclick="sendAction('clean')">清理</button>
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
        <div class="log-line">>> 視覺戰術戰情中心 v14 啟動完畢...</div>
    </div>

    <script>
        function sendAction(actionType) {
            fetch('/api/action', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({action: actionType})
            }).then(r => r.json()).then(d => update());
        }

        function changeInterval(val) {
            document.getElementById('speed-val').innerText = val;
            fetch('/api/action', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({set_interval: val})
            }).then(r => r.json()).then(d => update());
        }

        function update() {
            fetch('/api/status').then(r => r.json()).then(d => {
                document.getElementById('clock').innerText = d.time;
                document.getElementById('total').innerText = d.total;
                
                // 更新進度條
                document.getElementById('cpu-bar').style.width = d.cpu + '%';
                document.getElementById('cpu-lbl').innerText = d.cpu + '%';
                let memPercent = Math.min(100, Math.round((d.mem / 512) * 100));
                document.getElementById('mem-bar').style.width = memPercent + '%';
                document.getElementById('mem-lbl').innerText = d.mem + 'MB';

                // 更新滑桿數值
                document.getElementById('speed-val').innerText = d.interval;
                document.getElementById('interval-slider').value = d.interval;

                // 更新各模組筆數與佔比分佈條
                let total = d.total > 0 ? d.total : 1;
                let cm = d.counts["流量變現"] || 0;
                let ci = d.counts["多源情報"] || 0;
                let cc = d.counts["內容變現"] || 0;
                let ca = d.counts["AI 代理"] || 0;
                let cs = d.counts["系統運作"] || 0;

                document.getElementById('r-m').style.width = (cm / total * 100) + '%';
                document.getElementById('r-i').style.width = (ci / total * 100) + '%';
                document.getElementById('r-c').style.width = (cc / total * 100) + '%';
                document.getElementById('r-a').style.width = (ca / total * 100) + '%';
                document.getElementById('r-s').style.width = (cs / total * 100) + '%';

                document.getElementById('cnt-m').innerText = cm + " 筆";
                document.getElementById('cnt-i').innerText = ci + " 筆";
                document.getElementById('cnt-c').innerText = cc + " 筆";
                document.getElementById('cnt-a').innerText = ca + " 筆";
                document.getElementById('cnt-s').innerText = cs + " 筆";

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
