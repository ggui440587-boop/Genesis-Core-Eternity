from flask import Flask, jsonify
import threading
import time
import random

app = Flask(__name__)

# 模擬雙軌演化數據
state = {
    "pure_count": 9465,
    "pure_best": "PURE_AI_G3746_185",
    "pure_power": 93669,
    "hybrid_count": 7679,
    "hybrid_best": "HYBRID_OMEGA_6163",
    "hybrid_power": 306707,
    "paused": False,
    "leaderboard": [
        "HYBRID_OMEGA_6163",
        "HYBRID_OMEGA_9004",
        "HYBRID_OMEGA_7712",
        "HYBRID_OMEGA_7942",
        "HYBRID_OMEGA_3898",
        "HYBRID_OMEGA_8994",
        "HYBRID_OMEGA_1239",
        "HYBRID_OMEGA_8305"
    ]
}

def evolution_loop():
    while True:
        if not state["paused"]:
            state["pure_count"] += random.randint(1, 5)
            state["hybrid_count"] += random.randint(1, 5)
            state["hybrid_power"] += random.randint(0, 2)
        time.sleep(3)

threading.Thread(target=evolution_loop, daemon=True).start()

@app.route('/api/data')
def api_data():
    return jsonify(state)

@app.route('/')
def dashboard():
    return """
    <!DOCTYPE html>
    <html lang="zh-Hant">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>雙軌演化與產出分類實驗室</title>
        <style>
            body { background-color: #050811; color: #f1f5f9; font-family: monospace; padding: 12px; margin: 0; }
            h1 { color: #4ade80; text-align: center; font-size: 1.1rem; margin-bottom: 15px; }
            .card { background: #0f172a; border: 1px solid #1e293b; border-radius: 8px; padding: 12px; margin-bottom: 10px; }
            .pure-card { border-color: #22c55e; }
            .hybrid-card { border-color: #a855f7; }
            .btn { background: #ec4899; color: white; border: none; padding: 8px 16px; border-radius: 6px; font-weight: bold; cursor: pointer; margin-top: 8px; }
            .list-item { background: #1e293b; padding: 6px 10px; border-radius: 4px; margin-bottom: 4px; font-size: 0.8rem; border-left: 3px solid #facc15; }
        </style>
    </head>
    <body>
        <h1>🧬 雙軌演化與產出分類實驗室</h1>
        
        <div class="card pure-card">
            <p>🟢 同種純化軌道（產出數: <span id="p-count">9465</span>）</p>
            <p style="font-size:0.8rem; color:#94a3b8;">當前同種最強：<span id="p-best" style="color:#4ade80;">PURE_AI_G3746_185</span>（戰力: <span id="p-pow">93669</span>）</p>
            <p style="font-size:0.75rem; color:#22c55e;">🟢 同種純化成功：[AI模型與機器學習]<br><span id="p-best-2">PURE_AI_G3746_185</span></p>
        </div>
        
        <div class="card hybrid-card">
            <p>⚡ 混合融合軌道（產出數: <span id="h-count">7679</span>）</p>
            <p style="font-size:0.8rem; color:#94a3b8;">當前混合最強：<span id="h-best" style="color:#c084fc;">HYBRID_OMEGA_6163</span>（戰力: <span id="h-pow">306707</span>）</p>
            <p style="font-size:0.75rem; color:#c084fc;">⚡ 混合神獸產出：<span id="h-best-2">HYBRID_OMEGA_6163</span></p>
            <button class="btn" onclick="togglePause()" id="pause-btn">暫停雙軌</button>
        </div>

        <div class="card">
            <p style="color: #facc15;">🏆 雙軌產出戰力總榜</p>
            <div id="lb-container"></div>
        </div>

        <script>
            function updateUI() {
                fetch('/api/data')
                    .then(res => res.json())
                    .then(data => {
                        document.getElementById('p-count').innerText = data.pure_count;
                        document.getElementById('p-best').innerText = data.pure_best;
                        document.getElementById('p-best-2').innerText = data.pure_best;
                        document.getElementById('p-pow').innerText = data.pure_power;
                        
                        document.getElementById('h-count').innerText = data.hybrid_count;
                        document.getElementById('h-best').innerText = data.hybrid_best;
                        document.getElementById('h-best-2').innerText = data.hybrid_best;
                        document.getElementById('h-pow').innerText = data.hybrid_power;
                        
                        let lbHtml = '';
                        data.leaderboard.forEach((item, idx) => {
                            let score = data.hybrid_power - (idx * 30);
                            lbHtml += `<div class="list-item">[⚡ 混合] ${item} (全域混合) | 分數:${score}</div>`;
                        });
                        document.getElementById('lb-container').innerHTML = lbHtml;
                    });
            }
            function togglePause() {
                fetch('/toggle');
            }
            setInterval(updateUI, 2000);
            updateUI();
        </script>
    </body>
    </html>
    """

@app.route('/toggle')
def toggle():
    state["paused"] = not state["paused"]
    return jsonify({"paused": state["paused"]})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False)
