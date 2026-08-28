from flask import Flask, jsonify, request
import random, threading, time

app = Flask(__name__)

state = {
    "pure_count": 9465,
    "pure_best": "PURE_AI_G3746_185",
    "pure_score": 93669,
    "hybrid_count": 7679,
    "hybrid_best": "HYBRID_OMEGA_6163",
    "hybrid_score": 306707,
    "running": True,
    "leaderboard": [
        {"type": "混合", "name": "HYBRID_OMEGA_6163", "score": 306707},
        {"type": "混合", "name": "HYBRID_OMEGA_9004", "score": 306678},
        {"type": "混合", "name": "HYBRID_OMEGA_7712", "score": 306653},
        {"type": "混合", "name": "HYBRID_OMEGA_7942", "score": 306624},
        {"type": "混合", "name": "HYBRID_OMEGA_3898", "score": 306601},
        {"type": "混合", "name": "HYBRID_OMEGA_8994", "score": 306562},
        {"type": "混合", "name": "HYBRID_OMEGA_1239", "score": 306528},
        {"type": "混合", "name": "HYBRID_OMEGA_8305", "score": 306500}
    ]
}

def evolution_worker():
    global state
    while True:
        if state["running"]:
            state["pure_count"] += random.randint(1, 3)
            state["hybrid_count"] += random.randint(1, 3)
            state["pure_score"] += random.randint(-5, 10)
            state["hybrid_score"] += random.randint(-5, 15)
        time.sleep(2)

threading.Thread(target=evolution_worker, daemon=True).start()

@app.route('/api/status')
def api_status():
    return jsonify(state)

@app.route('/api/toggle', methods=['POST'])
def api_toggle():
    state["running"] = not state["running"]
    return jsonify({"running": state["running"]})

@app.route('/')
def index():
    return '''<!DOCTYPE html>
<html lang="zh-Hant">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>雙軌演化與產出分類實驗室</title>
    <style>
        body { background: #0b0b10; color: #e1e4e8; font-family: monospace; padding: 10px; margin: 0; }
        h2 { text-align: center; color: #00ff66; text-shadow: 0 0 8px rgba(0,255,102,0.4); font-size: 1.1rem; margin-bottom: 12px; }
        .card { background: #12121a; border: 1px solid #2a2a3d; border-radius: 8px; padding: 10px; margin-bottom: 10px; }
        .card-pure { border-color: #238636; }
        .card-hybrid { border-color: #a371f7; }
        .title { font-size: 0.85rem; font-weight: bold; margin-bottom: 6px; display: flex; align-items: center; gap: 6px; }
        .sub { font-size: 0.75rem; color: #8b949e; line-height: 1.4; }
        .highlight { color: #58a6ff; font-weight: bold; }
        .btn { background: #d21796; color: white; border: none; padding: 8px 16px; border-radius: 6px; font-family: monospace; font-weight: bold; font-size: 0.85rem; cursor: pointer; width: 100%; margin-top: 6px; box-shadow: 0 0 10px rgba(210,23,150,0.5); }
        .lb-item { background: #161622; border: 1px solid #222233; padding: 6px 8px; border-radius: 5px; margin-bottom: 5px; font-size: 0.72rem; display: flex; justify-content: space-between; align-items: center; }
        .lb-title { color: #f0883e; font-weight: bold; }
    </style>
</head>
<body>
    <h2>🧬 雙軌演化與產出分類實驗室</h2>
    
    <div class="card card-pure">
        <div class="title" style="color: #3fb950;">🟢 同種純化軌道（產出數: <span id="p-cnt">9465</span>）</div>
        <div class="sub">
            當前同種最強：<span id="p-best" class="highlight">PURE_AI_G3746_185</span> (戰力:<span id="p-score">93669</span>)<br>
            🟢 同種純化成功: [AI模型與機器學習]<br>
            <span id="p-sub-best" style="color: #7ee787;">PURE_AI_G3746_185</span>
        </div>
    </div>

    <div class="card card-hybrid">
        <div class="title" style="color: #a371f7;">⚡ 混合融合軌道（產出數: <span id="h-cnt">7679</span>）</div>
        <div class="sub">
            當前混合最強：<span id="h-best" class="highlight">HYBRID_OMEGA_6163</span> (戰力:<span id="h-score">306707</span>)<br>
            ⚡ 混合神獸產出: <span id="h-sub-best" style="color: #7ee787;">HYBRID_OMEGA_6163</span>
        </div>
        <button class="btn" id="toggle-btn" onclick="toggleRun()">暫停雙軌</button>
    </div>

    <div class="card" style="border-color: #f0883e;">
        <div class="title" style="color: #f0883e;">🏆 雙軌產出戰力總榜</div>
        <div id="lb-list">載入中...</div>
    </div>

    <script>
        function toggleRun() {
            fetch('/api/toggle', {method: 'POST'}).then(r => r.json()).then(d => {
                document.getElementById('toggle-btn').innerText = d.running ? '暫停雙軌' : '恢復雙軌';
                document.getElementById('toggle-btn').style.background = d.running ? '#d21796' : '#238636';
            });
        }
        function update() {
            fetch('/api/status').then(r => r.json()).then(d => {
                document.getElementById('p-cnt').innerText = d.pure_count;
                document.getElementById('p-best').innerText = d.pure_best;
                document.getElementById('p-score').innerText = d.pure_score;
                document.getElementById('p-sub-best').innerText = d.pure_best;
                
                document.getElementById('h-cnt').innerText = d.hybrid_count;
                document.getElementById('h-best').innerText = d.hybrid_best;
                document.getElementById('h-score').innerText = d.hybrid_score;
                document.getElementById('h-sub-best').innerText = d.hybrid_best;

                let html = '';
                d.leaderboard.forEach(item => {
                    html += '<div class="lb-item"><span class="lb-title">[⚡ ' + item.type + '] ' + item.name + '</span><span>(全域混合) │ 分數:' + item.score + '</span></div>';
                });
                document.getElementById('lb-list').innerHTML = html;
            });
        }
        setInterval(update, 2000);
        update();
    </script>
</body>
</html>'''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8082, debug=False)
