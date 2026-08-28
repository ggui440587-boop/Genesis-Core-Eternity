import time
import threading
import sqlite3
import json
import datetime
import subprocess
import sys
import importlib
import requests
import os
import zipfile
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

DB_NAME = 'smart_engine.db'
WEB_PORT = 5050
LLM_MODEL = 'qwen2.5:latest'
OLLAMA_URL = 'http://127.0.0.1:11434/api/generate'

# Telegram 告警設定
TELEGRAM_BOT_TOKEN = os.environ.get('TG_BOT_TOKEN', '')
TELEGRAM_CHAT_ID = os.environ.get('TG_CHAT_ID', '')

# 聯盟行銷追蹤碼設定 (可替換為你的 Shopee / iChannels ID)
AFFILIATE_TAG = os.environ.get('AFFILIATE_TAG', 'genesis_2026_20')

def send_telegram_alert(message):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print(f"[Telegram 模擬推播]: {message}")
        return
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "Markdown"}
        requests.post(url, json=payload, timeout=5)
    except Exception as e:
        print(f"Telegram 推播失敗: {e}")

# --- 1. 聯盟行銷與分潤連結自動注入器 ---
def inject_affiliate_links(text):
    # 模擬自動將文章中的關鍵字或結尾包裝為 Shopee / iChannels 分潤連結
    affiliate_footer = f"\n\n🔥 **精選好物推薦與支援**：\n- 立即查看熱門工具與裝備：[點擊這裡解鎖專屬優惠](https://s.shopee.tw/affiliate?tag={AFFILIATE_TAG})\n- 透過聯盟通路支持本自動化引擎持續運作！"
    return text + affiliate_footer

# --- 2. 多模型協同 (Swarm Router) ---
def ask_specialized_agent(role_prompt, task_text):
    full_prompt = f"【角色設定：{role_prompt}】\n請根據以下任務進行深度處理：\n{task_text}"
    try:
        payload = {
            "model": LLM_MODEL,
            "prompt": full_prompt,
            "stream": False,
            "options": {"temperature": 0.6, "num_predict": 250}
        }
        res = requests.post(OLLAMA_URL, json=payload, timeout=30)
        if res.status_code == 200:
            return res.json().get('response', '模型無回應')
    except Exception as e:
        return f"模型協同錯誤: {e}"
    return "模型逾時"

# --- 3. 多源情報與智慧擴張 ---
def fetch_multi_source_intels():
    intels = []
    try:
        res = requests.get('https://hacker-news.firebaseio.com/v0/topstories.json', timeout=5)
        if res.status_code == 200:
            top_id = res.json()[0]
            item = requests.get(f'https://hacker-news.firebaseio.com/v0/item/{top_id}.json', timeout=3).json()
            intels.append(f"[HN 焦點] {item.get('title', '')}")
    except: pass

    try:
        res = requests.get('https://api.github.com/search/repositories?q=stars:>1000&sort=stars&order=desc', timeout=5)
        if res.status_code == 200:
            repo = res.json()['items'][0]
            intels.append(f"[開源金礦] {repo['full_name']} - {repo['description']}")
    except: pass

    return " | ".join(intels) if intels else "多源情報同步中..."

def perform_system_backup():
    try:
        backup_dir = 'backups'
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_path = os.path.join(backup_dir, f'smart_backup_{timestamp}.zip')
        
        with zipfile.ZipFile(backup_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            if os.path.exists(DB_NAME):
                zipf.write(DB_NAME)
            if os.path.exists('ultimate_smart_engine.py'):
                zipf.write('ultimate_smart_engine.py')
        return f"系統自動備份成功: {backup_path}"
    except Exception as e:
        return f"備份失敗: {e}"

# --- 4. 代理迴圈：Scout (情報採集) ---
def scout_agent_loop():
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS smart_intels
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
                  agent TEXT, event TEXT, details TEXT, cycles INTEGER)''')
    conn.commit()
    
    cycle = 0
    while True:
        cycle += 1
        print(f'\n[SWARM Scout] 第 {cycle} 輪多源情報採集...')
        
        intel = fetch_multi_source_intels()
        c.execute("INSERT INTO smart_intels (agent, event, details, cycles) VALUES (?, ?, ?, ?)", 
                  ('SCOUT', 'MULTI_INTEL', intel, cycle))
        conn.commit()
        time.sleep(30)

# --- 5. 代理迴圈：Coder (系統與備份) ---
def coder_agent_loop():
    time.sleep(5)
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    c = conn.cursor()
    
    cycle = 0
    while True:
        cycle += 1
        time.sleep(45)
        print(f'\n[SWARM Coder] 第 {cycle} 輪系統安全維護...')
        
        backup_status = perform_system_backup()
        c.execute("INSERT INTO smart_intels (agent, event, details, cycles) VALUES (?, ?, ?, ?)", 
                  ('CODER', 'SYS_MAINTENANCE', backup_status, cycle))
        conn.commit()

# --- 6. 代理迴圈：Publisher (分潤文案生成與自動發布) ---
def publisher_agent_loop():
    time.sleep(10)
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    c = conn.cursor()
    
    cycle = 0
    while True:
        cycle += 1
        time.sleep(60)
        print(f'\n[AFFILIATE Publisher] 第 {cycle} 輪聯盟行銷變現流生成...')
        
        role = "頂級聯盟行銷與流量變現專家，擅長將科技潮流與變現文案完美融合"
        task = "分析當前趨勢，生成一篇具備高轉換率的繁體中文推廣短文。"
        raw_content = ask_specialized_agent(role, task)
        
        # 自動注入分潤連結
        final_monetize_content = inject_affiliate_links(raw_content)
        
        # 觸發 Telegram 推播
        send_telegram_alert(f"💰 *自動化聯盟行銷分潤文案發布*\n\n{final_monetize_content[:250]}...")
        
        c.execute("INSERT INTO smart_intels (agent, event, details, cycles) VALUES (?, ?, ?, ?)", 
                  ('PUBLISHER', 'AFFILIATE_FLOW', final_monetize_content.replace('\n', ' '), cycle))
        conn.commit()

# --- 7. 網頁戰情室 (完全商業變現版) ---
HTML_TEMPLATE = """<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta http-equiv="refresh" content="15">
    <title>聯盟行銷與自動化變現終極戰情室</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        * { box-sizing: border-box; }
        body { background: #05070c; color: #ffffff; font-family: 'Segoe UI', Roboto, sans-serif; margin: 0; padding: 16px; min-height: 100vh; }
        .header { background: linear-gradient(135deg, #831843 0%, #0f172a 100%); border: 3px solid #f43f5e; border-radius: 22px; padding: 28px; text-align: center; margin-bottom: 22px; box-shadow: 0 0 30px rgba(244,63,94,0.4); }
        .header h1 { font-size: 32px; color: #f43f5e; margin: 0 0 12px 0; font-weight: 900; text-shadow: 0 0 20px rgba(244,63,94,0.8); }
        .header p { font-size: 20px; color: #e2e8f0; margin: 0; font-weight: 800; display: flex; align-items: center; justify-content: center; gap: 12px; }
        .pulse { width: 18px; height: 18px; background-color: #4ade80; border-radius: 50%; display: inline-block; box-shadow: 0 0 15px #4ade80; animation: pulse 1.2s infinite; }
        @keyframes pulse { 0% { transform: scale(0.9); opacity: 0.7; } 50% { transform: scale(1.4); opacity: 1; } 100% { transform: scale(0.9); opacity: 0.7; } }
        
        .grid { display: flex; flex-direction: column; gap: 24px; }
        .card { background: #0f172a; border: 3px solid #334155; border-radius: 22px; padding: 26px; box-shadow: 0 8px 30px rgba(0,0,0,0.6); position: relative; overflow: hidden; }
        .card::before { content: ''; position: absolute; top: 0; left: 0; width: 10px; height: 100%; background: #f43f5e; }
        
        h2 { color: #f43f5e; font-size: 26px; border-bottom: 3px solid #1e293b; padding-bottom: 14px; margin-top: 0; font-weight: 900; letter-spacing: 1px; }
        p { font-size: 24px; line-height: 1.6; margin: 16px 0; color: #f8fafc; font-weight: 800; }
        .stat-value { font-size: 48px; font-weight: 900; color: #4ade80; text-shadow: 0 0 20px rgba(74,222,128,0.6); }
        
        .interactive-form { display: flex; gap: 12px; margin-top: 16px; flex-wrap: wrap; }
        input[type="text"] { flex: 1; min-width: 250px; padding: 16px; font-size: 20px; border-radius: 12px; border: 3px solid #475569; background: #090d16; color: #ffffff; font-weight: bold; }
        button { padding: 16px 28px; font-size: 20px; font-weight: 900; background: #f43f5e; color: #0f172a; border: none; border-radius: 12px; cursor: pointer; box-shadow: 0 0 15px rgba(244,63,94,0.5); }
        button:active { transform: scale(0.98); }
        
        .chart-container { position: relative; width: 100%; height: 300px; margin-top: 18px; }
        .table-container { width: 100%; overflow-x: auto; -webkit-overflow-scrolling: touch; margin-top: 18px; border-radius: 14px; border: 3px solid #334155; }
        table { width: 100%; border-collapse: collapse; min-width: 450px; }
        th, td { padding: 18px 20px; text-align: left; font-size: 22px; font-weight: 800; }
        th { background: #1e293b; color: #f43f5e; border-bottom: 4px solid #334155; }
        td { color: #ffffff; background: #090d16; border-bottom: 3px solid #1e293b; }
        pre { margin: 0; color: #4ade80; white-space: pre-wrap; word-break: break-all; font-family: monospace; font-size: 20px; font-weight: 900; line-height: 1.5; }
    </style>
</head>
<body>
    <div class="header">
        <h1>💰 聯盟行銷與自動化變現終極戰情室 💰</h1>
        <p><span class="pulse"></span> Shopee/iChannels 分潤連結自動注入 + Swarm 協同 + 即時戰情互動</p>
    </div>
    
    <div class="grid">
        <div class="card">
            <h2>系統全域概況與分潤指令中樞</h2>
            <p>總循環次數: <span class="stat-value">__CYCLES__</span></p>
            <p>系統狀態: <span style="color: #4ade80;">商業變現完全體運作 (Affiliate Ultimate)</span></p>
            
            <form class="interactive-form" method="GET" action="/">
                <input type="text" name="cmd" placeholder="輸入商業變現或分潤文案指令..." required>
                <button type="submit">執行調用</button>
            </form>
            __CMD_RESULT__
        </div>
        
        <div class="card" style="border-left-color: #38bdf8;">
            <h2>變現與情報活動增長趨勢圖</h2>
            <div class="chart-container">
                <canvas id="cycleChart"></canvas>
            </div>
        </div>
    </div>

    <div class="card" style="margin-top: 24px; border-left-color: #fbbf24;">
        <h2>聯盟行銷與情報產出日誌</h2>
        <div class="table-container">
            <table>
                <tr><th>時間</th><th>代理身分 (Agent)</th><th>事件與內容</th></tr>
                __TABLE_ROWS__
            </table>
        </div>
    </div>

    <script>
        const ctx = document.getElementById('cycleChart').getContext('2d');
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: __CHART_LABELS__,
                datasets: [{
                    label: '變現與情報活動量',
                    data: __CHART_DATA__,
                    borderColor: '#f43f5e',
                    backgroundColor: 'rgba(244, 63, 94, 0.15)',
                    borderWidth: 4,
                    fill: true,
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { labels: { color: '#f8fafc', font: { size: 16, weight: 'bold' } } } },
                scales: {
                    x: { ticks: { color: '#cbd5e1', font: { size: 14 } }, grid: { color: 'rgba(255,255,255,0.08)' } },
                    y: { ticks: { color: '#cbd5e1', font: { size: 14 } }, grid: { color: 'rgba(255,255,255,0.08)' } }
                }
            }
        });
    </script>
</body>
</html>
"""

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        query_params = parse_qs(parsed_path.query)
        
        cmd_result_html = ""
        if 'cmd' in query_params:
            user_cmd = query_params['cmd'][0]
            raw_ans = ask_specialized_agent("資深商業變現與流量轉換架構師", user_cmd)
            ai_ans = inject_affiliate_links(raw_ans)
            cmd_result_html = f"<div style='margin-top:20px; padding:18px; background:#1e293b; border-radius:12px; border:2px solid #f43f5e;'><strong style='color:#f43f5e;'>變現與分潤回應:</strong><p style='margin:8px 0 0 0; font-size:20px; color:#ffffff;'>{ai_ans}</p></div>"
            
            conn = sqlite3.connect(DB_NAME, check_same_thread=False)
            c = conn.cursor()
            c.execute("INSERT INTO smart_intels (agent, event, details, cycles) VALUES (?, ?, ?, ?)", 
                      ('USER', 'AFFILIATE_CMD', f"指令: {user_cmd} | 回應: {ai_ans[:60]}...", 999))
            conn.commit()

        if parsed_path.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            
            conn = sqlite3.connect(DB_NAME, check_same_thread=False)
            c = conn.cursor()
            
            c.execute("SELECT COUNT(DISTINCT cycles) FROM smart_intels WHERE cycles != 999")
            res_cycles = c.fetchone()
            total_cycles = res_cycles[0] if res_cycles and res_cycles[0] else 0

            c.execute("SELECT ts, agent, details FROM smart_intels ORDER BY id DESC LIMIT 14")
            rows = c.fetchall()
            table_rows = ""
            for r in rows:
                color_map = {'SCOUT': '#38bdf8', 'CODER': '#4ade80', 'PUBLISHER': '#f43f5e', 'USER': '#facc15'}
                c_color = color_map.get(r[1], '#ffffff')
                table_rows += f"<tr><td>{r[0]}</td><td style='color:{c_color};'>{r[1]}</td><td><pre>{r[2]}</pre></td></tr>"
            if not table_rows:
                table_rows = "<tr><td colspan='3'>戰情室初始化中...</td></tr>"

            c.execute("SELECT ts, cycles FROM smart_intels WHERE cycles != 999 ORDER BY id ASC LIMIT 10")
            history = c.fetchall()
            chart_labels = [h[0].split(' ')[-1] for h in history] if history else ['0']
            chart_data = [h[1] for h in history] if history else [0]

            html = HTML_TEMPLATE.replace("__CYCLES__", str(total_cycles))\
                                .replace("__CMD_RESULT__", cmd_result_html)\
                                .replace("__TABLE_ROWS__", table_rows)\
                                .replace("__CHART_LABELS__", json.dumps(chart_labels))\
                                .replace("__CHART_DATA__", json.dumps(chart_data))
            self.wfile.write(html.encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

def run_server():
    server_address = ('127.0.0.1', WEB_PORT)
    httpd = HTTPServer(server_address, RequestHandler)
    print(f'[+] 聯盟行銷終極戰情室已啟動於 http://127.0.0.1:{WEB_PORT}')
    httpd.serve_forever()

if __name__ == '__main__':
    t1 = threading.Thread(target=scout_agent_loop, daemon=True)
    t2 = threading.Thread(target=coder_agent_loop, daemon=True)
    t3 = threading.Thread(target=publisher_agent_loop, daemon=True)
    
    t1.start()
    t2.start()
    t3.start()
    
    run_server()
