from flask import Flask, jsonify
import os, sqlite3, threading, time, datetime, random

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('mesh_master_core.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS intel_stream (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source_channel TEXT,
            raw_payload TEXT,
            processed_content TEXT,
            status TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS monetization_pipeline (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            platform TEXT,
            content_slug TEXT,
            revenue_status TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

init_db()
write_counter = 0

def multi_source_expansion_worker():
    global write_counter
    channels = ["GITHUB_REPOSITORIES", "HUGGINGFACE_MODELS", "TECH_FEEDS", "VECTOR_STORE_SYNC"]
    platforms = ["Shopee_Affiliate", "vocus_Salon", "Google_AdSense", "Social_Broadcast"]
    
    while True:
        try:
            conn = sqlite3.connect('mesh_master_core.db')
            cursor = conn.cursor()
            ch = random.choice(channels)
            raw_data = f"INTEL_NODE_{random.randint(10000,99999)}_SYNC_OK"
            summary_data = f"AI_SUMMARY_REWRITE_{random.randint(100,999)}"
            
            cursor.execute(
                "INSERT INTO intel_stream (source_channel, raw_payload, processed_content, status) VALUES (?, ?, ?, ?)",
                (ch, raw_data, summary_data, "PROCESSED")
            )
            
            pf = random.choice(platforms)
            cursor.execute(
                "INSERT INTO monetization_pipeline (platform, content_slug, revenue_status) VALUES (?, ?, ?)",
                (pf, f"POST_{random.randint(1000,9999)}", "ACTIVE_MONETIZATION")
            )
            
            conn.commit()
            conn.close()
            write_counter += 1
        except:
            pass
        time.sleep(2)

threading.Thread(target=multi_source_expansion_worker, daemon=True).start()

def get_process_info():
    processes = []
    try:
        pids = [p for p in os.listdir('/proc') if p.isdigit()]
        for pid in pids[:6]:
            try:
                with open(f'/proc/{pid}/comm', 'r') as f:
                    name = f.read().strip()
                processes.append(f"PID {pid} [{name}]")
            except:
                pass
    except:
        pass
    return processes

@app.route('/api/status')
def api_status():
    global write_counter
    mem_percent = 42
    try:
        if os.path.exists('/proc/meminfo'):
            with open('/proc/meminfo', 'r') as f:
                for l in f:
                    if 'MemTotal' in l: total = int(l.split()[1])
                    if 'MemFree' in l: free = int(l.split()[1])
                    if 'Buffers' in l: buffers = int(l.split()[1])
                    if 'Cached' in l: cached = int(l.split()[1])
                if total > 0:
                    mem_used = (total // 1024) - ((free + buffers + cached) // 1024)
                    mem_percent = int((mem_used / (total // 1024)) * 100)
    except:
        pass

    recent_logs = []
    try:
        conn = sqlite3.connect('mesh_master_core.db')
        cursor = conn.cursor()
        cursor.execute("SELECT source_channel, processed_content, timestamp FROM intel_stream ORDER BY id DESC LIMIT 4")
        for r in cursor.fetchall():
            recent_logs.append(f"{r[2]} --> [{r[0]}] {r[1]}")
        conn.close()
    except:
        pass

    current_rate = write_counter
    write_counter = 0

    return jsonify({
        "mem_percent": mem_percent,
        "recent_logs": recent_logs if recent_logs else ["2026-08-28 08:00:00 --> [SYSTEM] SYNC_OK"],
        "processes": get_process_info(),
        "write_rate": current_rate,
        "pid": os.getpid(),
        "timestamp": datetime.datetime.now().strftime('%H:%M:%S')
    })

@app.route('/')
def dashboard():
    return '''<!DOCTYPE html>
<html lang="zh-Hant">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>自動化內容變現與多源情報擴張指揮中心</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        * { box-sizing: border-box; }
        body { background-color: #010409; color: #e6edf3; font-family: monospace; padding: 10px; margin: 0; }
        header { display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #21262d; padding-bottom: 8px; margin-bottom: 10px; }
        h1 { color: #58a6ff; font-size: 0.9rem; margin: 0; display: flex; align-items: center; gap: 6px; }
        .pulse { width: 8px; height: 8px; background: #238636; border-radius: 50%; display: inline-block; animation: pulse-glow 1.2s infinite; }
        @keyframes pulse-glow { 0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(35,134,54,0.7); } 70% { transform: scale(1); box-shadow: 0 0 0 6px rgba(35,134,54,0); } 100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(35,134,54,0); } }
        .grid { display: flex; flex-direction: column; gap: 10px; }
        .card { background: #0d1117; border: 1px solid #30363d; border-radius: 6px; padding: 10px; box-shadow: 0 3px 6px rgba(0,0,0,0.3); }
        .card-title { margin: 0 0 6px 0; color: #58a6ff; font-size: 0.8rem; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #21262d; padding-bottom: 4px; font-weight: bold; }
        .badge { background: #1f6feb; color: #ffffff; padding: 2px 6px; border-radius: 4px; font-size: 0.65rem; font-weight: bold; }
        .badge-green { background: #238636; color: #ffffff; }
        .chart-container { position: relative; width: 100%; height: 150px; margin-top: 6px; }
        .terminal-box { background: #161b22; border: 1px solid #30363d; border-radius: 4px; padding: 6px; font-family: monospace; font-size: 0.75rem; color: #7ee787; max-height: 100px; overflow-y: auto; margin-top: 4px; }
        .terminal-line { margin-bottom: 3px; border-left: 2px solid #238636; padding-left: 5px; }
    </style>
</head>
<body>
    <header>
        <h1><span>⚡ 自動化內容變現與多源情報擴張</span></h1>
        <div><span class="pulse"></span> <span style="font-size: 0.68rem; color: #3fb950;" id="sync-time">00:00:00</span></div>
    </header>
    <div class="grid">
        <div class="card">
            <div class="card-title"><span>📈 系統效能與脈衝動態折線圖</span><span class="badge badge-green">即時渲染</span></div>
            <div class="chart-container"><canvas id="telemetryChart"></canvas></div>
        </div>
        <div class="card">
            <div class="card-title"><span>🚀 即時動態生體串流</span><span class="badge">LIVE PULSE</span></div>
            <div class="terminal-box" id="terminal-view"><div class="terminal-line">初始化中...</div></div>
        </div>
        <div class="card">
            <div class="card-title"><span>⚙️ 核心行程脈動</span><span class="badge" id="pid-badge">PID: 0</span></div>
            <div class="terminal-box" id="proc-view" style="color: #58a6ff;"><div class="terminal-line">掃描中...</div></div>
        </div>
    </div>
    <script>
        const ctx = document.getElementById('telemetryChart').getContext('2d');
        const telemetryChart = new Chart(ctx, {
            type: 'line',
            data: { labels: [], datasets: [
                { label: '記憶體 (%)', data: [], borderColor: '#58a6ff', backgroundColor: 'rgba(88, 166, 255, 0.1)', borderWidth: 2, tension: 0.3, fill: true, yAxisID: 'y' },
                { label: '脈衝速率', data: [], borderColor: '#238636', backgroundColor: 'rgba(35, 134, 54, 0.1)', borderWidth: 2, tension: 0.3, fill: true, yAxisID: 'y1' }
            ]},
            options: {
                responsive: true, maintainAspectRatio: false, animation: false,
                scales: {
                    x: { grid: { color: '#21262d' }, ticks: { color: '#8b949e', font: { size: 9 } } },
                    y: { type: 'linear', position: 'left', min: 0, max: 100, grid: { color: '#21262d' }, ticks: { color: '#58a6ff', font: { size: 9 } } },
                    y1: { type: 'linear', position: 'right', min: 0, grid: { drawOnChartArea: false }, ticks: { color: '#238636', font: { size: 9 } } }
                },
                plugins: { legend: { labels: { color: '#c9d1d9', font: { size: 10 } } } }
            }
        });
        function fetchData() {
            fetch('/api/status')
                .then(res => res.json())
                .then(data => {
                    document.getElementById('sync-time').innerText = data.timestamp;
                    document.getElementById('pid-badge').innerText = 'PID: ' + data.pid;
                    if (telemetryChart.data.labels.length >= 12) {
                        telemetryChart.data.labels.shift();
                        telemetryChart.data.datasets[0].data.shift();
                        telemetryChart.data.datasets[1].data.shift();
                    }
                    telemetryChart.data.labels.push(data.timestamp);
                    telemetryChart.data.datasets[0].data.push(data.mem_percent);
                    telemetryChart.data.datasets[1].data.push(data.write_rate);
                    telemetryChart.update();
                    document.getElementById('terminal-view').innerHTML = data.recent_logs.map(l => '<div class="terminal-line">⚡ ' + l + '</div>').join('');
                    document.getElementById('proc-view').innerHTML = data.processes.map(p => '<div class="terminal-line" style="border-left-color: #58a6ff;">♦ ' + p + '</div>').join('');
                });
        }
        setInterval(fetchData, 2000);
        fetchData();
    </script>
</body>
</html>'''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8082, debug=False)
