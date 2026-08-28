from flask import Flask, jsonify
import os, sqlite3, threading, time, datetime, random

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('mesh_matrix.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS stream (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            val TEXT,
            ts DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

init_db()
counter = 0

def loop():
    global counter
    while True:
        try:
            conn = sqlite3.connect('mesh_matrix.db')
            cursor = conn.cursor()
            num_code = f"{random.randint(10000000,99999999)}"
            cursor.execute("INSERT INTO stream (val) VALUES (?)", (num_code,))
            conn.commit()
            conn.close()
            counter += 1
        except:
            pass
        time.sleep(2)

threading.Thread(target=loop, daemon=True).start()

@app.route('/api/status')
def status():
    global counter
    logs = []
    try:
        conn = sqlite3.connect('mesh_matrix.db')
        cursor = conn.cursor()
        cursor.execute("SELECT val, ts FROM stream ORDER BY id DESC LIMIT 5")
        for r in cursor.fetchall():
            t = r[1].replace('-', '').replace(':', '').replace(' ', '')[-6:]
            logs.append(f"{t} : {r[0]}")
        conn.close()
    except:
        pass

    rate = counter
    counter = 0

    procs = []
    try:
        for p in os.listdir('/proc'):
            if p.isdigit():
                procs.append(f"{p} : {abs(hash(p)) % 900000 + 100000}")
                if len(procs) >= 6: break
    except:
        pass

    return jsonify({
        "logs": logs if logs else ["000000 : 00000000"],
        "procs": procs,
        "pid": os.getpid(),
        "time": datetime.datetime.now().strftime('%H:%M:%S')
    })

@app.route('/')
def index():
    return '''<!DOCTYPE html>
<html lang="zh-Hant">
<head>
    <meta charset="UTF-8">
    <title>0000</title>
    <style>
        body { background: #010409; color: #7ee787; font-family: monospace; padding: 10px; margin: 0; }
        .card { background: #0d1117; border: 1px solid #30363d; border-radius: 4px; padding: 10px; margin-bottom: 8px; }
        .line { margin-bottom: 4px; border-left: 2px solid #238636; padding-left: 6px; letter-spacing: 1px; }
    </style>
</head>
<body>
    <div style="font-size: 1rem; color: #58a6ff; margin-bottom: 8px;">0000-0000 // <span id="t">00:00:00</span></div>
    <div class="card">
        <div id="logs"></div>
    </div>
    <div class="card">
        <div id="procs"></div>
    </div>
    <script>
        function update() {
            fetch('/api/status').then(r => r.json()).then(d => {
                document.getElementById('t').innerText = d.time;
                document.getElementById('logs').innerHTML = d.logs.map(l => '<div class="line">' + l + '</div>').join('');
                document.getElementById('procs').innerHTML = d.procs.map(p => '<div class="line" style="border-left-color: #58a6ff;">' + p + '</div>').join('');
            });
        }
        setInterval(update, 2000);
        update();
    </script>
</body>
</html>'''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8082, debug=False)
