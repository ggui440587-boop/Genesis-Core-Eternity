from flask import Flask, jsonify
import random

app = Flask(__name__)
state = {
    "counts": {"AI模型與機器學習": 3420, "自動化系統": 2890},
    "logs": ["[INFO] 戰情中心獨立守護中"]
}

@app.route('/api/status')
def api_status():
    return jsonify(state)

@app.route('/')
def index():
    return '''<!DOCTYPE html>
<html lang="zh-Hant"><head><meta charset="UTF-8"><title>Ultimate V15 戰情室</title>
<style>body{background:#05050a;color:#cfd8dc;font-family:monospace;padding:10px;margin:0;}h2{color:#00ffcc;text-align:center;}</style>
</head><body><h2>⚡ Genesis Ultimate V15 戰情中心</h2><div style="background:#0d0d14;border:1px solid #1f1f2e;padding:10px;border-radius:8px;">戰情室核心運作中...</div></body></html>'''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8082, debug=False)
