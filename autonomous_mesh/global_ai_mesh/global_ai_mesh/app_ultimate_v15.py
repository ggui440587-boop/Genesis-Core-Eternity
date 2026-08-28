from flask import Flask, jsonify, request
import random, threading, time, os

app = Flask(__name__)

# 模擬戰情室與終端日誌狀態
state = {
    "counts": {"AI模型與機器學習": 3420, "自動化系統": 2890, "網路情報": 1940},
    "sections": {
        "AI模型與機器學習": ["Genesis-Core-Eternity 核心初始化完成", "Hugging Face 節點中繼連線穩定", "模型微調參數自動校準"],
        "自動化系統": ["背景行程 nohup 守護中", "排程任務同步執行", "SQLite 資料庫寫入正常"],
        "網路情報": ["多源情報擴張通道開啟", "API 數據包自動抓取", "防禦牆隔離機制確認"]
    },
    "history": {
        "AI模型與機器學習": [10, 25, 40, 35, 60, 85, 90],
        "自動化系統": [15, 30, 45, 50, 65, 70, 88],
        "網路情報": [5, 12, 20, 35, 40, 55, 72]
    },
    "logs": [
        "[INFO] 2026-08-28 08:50:00 - 系統運行穩定",
        "[SUCCESS] 2026-08-28 08:50:09 - 數據同步完成",
        "[WATCH] 2026-08-28 08:50:20 - 背景程序監聽中"
    ]
}

@app.route('/api/status')
def api_status():
    return jsonify(state)

@app.route('/')
def index():
    return '''<!DOCTYPE html>
<html lang="zh-Hant">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Genesis Ultimate V15 戰情室</title>
    <style>
        body { background: #05050a; color: #cfd8dc; font-family: monospace; padding: 10px; margin: 0; }
        h2 { text-align: center; color: #00ffcc; text-shadow: 0 0 10px rgba(0,255,204,0.4); font-size: 1.1rem; margin-bottom: 15px; }
        .card { background: #0d0d14; border: 1px solid #1f1f2e; border-radius: 8px; padding: 12px; margin-bottom: 12px; }
        .title { font-size: 0.85rem; font-weight: bold; color: #79c0ff; margin-bottom: 8px; }
        .bar-container { background: #161622; border-radius: 4px; overflow: hidden; height: 8px; margin-top: 5px; margin-bottom: 8px; }
        .bar-fill { background: linear-gradient(90deg, #1f6feb, #58a6ff); height: 100%; width: 0%; transition: width 0.5s; }
        .item { font-size: 0.72rem; color: #8b949e; padding: 2px 0; border-bottom: 1px dashed #161622; }
        .log-box { background: #08080c; border: 1px solid #161622; padding: 8px; border-radius: 6px; font-size: 0.7rem; color: #3fb950; max-height: 120px; overflow-y: auto; }
    </style>
</head>
<body>
    <h2>⚡ Genesis Ultimate V15 戰情中心</h2>
    
    <div class="card">
        <div class="title">📊 分類數據監控</div>
        <div id="metrics"></div>
    </div>

    <div class="card">
        <div class="title">💻 即時終端日誌 (Terminal Logs)</div>
        <div class="log-box" id="log-box">載入中...</div>
    </div>

    <script>
        function update() {
            fetch('/api/status').then(r => r.json()).then(d => {
                let cats = Object.keys(d.counts);
                let tot = cats.reduce((sum, k) => sum + d.counts[k], 0) || 1;
                let html = '';
                cats.forEach((catName, idx) => {
                    let count = d.counts[catName] || 0;
                    let pct = (count / tot * 100).toFixed(1);
                    html += '<div style="margin-bottom:8px;"><div style="display:flex; justify-content:space-between; font-size:0.75rem;"><span>' + catName + '</span><span style="color:#f0883e;">' + count + ' 筆 (' + pct + '%)</span></div>';
                    html += '<div class="bar-container"><div class="bar-fill" style="width:' + pct + '%;"></div></div>';
                    let items = d.sections[catName] || [];
                    items.forEach(i => { html += '<div class="item">🔹 ' + i + '</div>'; });
                    html += '</div>';
                });
                document.getElementById('metrics').innerHTML = html;

                if (d.logs) {
                    document.getElementById('log-box').innerHTML = d.logs.join('<br>');
                }
            });
        }
        setInterval(update, 3000);
        update();
    </script>
</body>
</html>'''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8082, debug=False)
