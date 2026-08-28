from flask import Flask, jsonify, request
import random, threading, time

app = Flask(__name__)
state = {
    "pure_count": 9465, "pure_best": "PURE_AI_G3746_185", "pure_score": 93669,
    "hybrid_count": 7679, "hybrid_best": "HYBRID_OMEGA_6163", "hybrid_score": 306707,
    "running": True,
    "leaderboard": [
        {"type": "混合", "name": "HYBRID_OMEGA_6163", "score": 306707},
        {"type": "混合", "name": "HYBRID_OMEGA_9004", "score": 306678}
    ]
}

def evolution_worker():
    global state
    while True:
        if state["running"]:
            state["pure_count"] += random.randint(1, 3)
            state["hybrid_count"] += random.randint(1, 3)
        time.sleep(2)

threading.Thread(target=evolution_worker, daemon=True).start()

@app.route('/api/status')
def api_status():
    return jsonify(state)

@app.route('/')
def index():
    return '''<!DOCTYPE html>
<html lang="zh-Hant"><head><meta charset="UTF-8"><title>雙軌演化實驗室</title>
<style>body{background:#0b0b10;color:#e1e4e8;font-family:monospace;padding:10px;margin:0;}h2{color:#00ff66;text-align:center;}</style>
</head><body><h2>🧬 雙軌演化與產出分類實驗室</h2><div style="background:#12121a;border:1px solid #238636;padding:10px;border-radius:8px;">同種純化軌道運行中... 產出數: <span id="cnt">9465</span></div>
<script>setInterval(()=>{fetch('/api/status').then(r=>r.json()).then(d=>document.getElementById('cnt').innerText=d.pure_count)},2000);</script>
</body></html>'''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False)
