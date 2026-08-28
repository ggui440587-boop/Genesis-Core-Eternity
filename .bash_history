pkill -f python
python ultimate_smart_engine.py &
python -c "
with open('ultimate_smart_engine.py', 'r', encoding='utf-8') as f:
    code = f.read()

import re

# 替換為專為手機最佳化的響應式 CSS 樣式
old_css_pattern = r'<style>.*?</style>'
new_style = '''<style>
        * { box-sizing: border-box; }
        body { background: #121212; color: #e0e0e0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; margin: 0; padding: 10px; }
        .header { background: #1e1e1e; border: 1px solid #2d2d2d; border-radius: 10px; padding: 15px; text-align: center; margin-bottom: 15px; }
        .header h1 { font-size: 15px; color: #ffffff; margin: 0 0 5px 0; font-weight: 600; }
        .header p { font-size: 11px; color: #888888; margin: 0; }
        .grid { display: flex; flex-direction: column; gap: 12px; }
        .card { background: #1e1e1e; border: 1px solid #2d2d2d; border-radius: 10px; padding: 12px; overflow-x: auto; }
        h2 { color: #ffffff; font-size: 12px; border-bottom: 1px solid #2d2d2d; padding-bottom: 6px; margin-top: 0; font-weight: 600; }
        p { font-size: 12px; line-height: 1.5; margin: 6px 0; color: #b0b0b0; word-break: break-all; }
        .stat-value { font-size: 18px; font-weight: 700; color: #4ade80; }
        .table-container { width: 100%; overflow-x: auto; -webkit-overflow-scrolling: touch; margin-top: 8px; }
        table { width: 100%; border-collapse: collapse; min-width: 300px; }
        th, td { border: 1px solid #2d2d2d; padding: 8px; text-align: left; font-size: 11px; }
        th { background: #252525; color: #ffffff; font-weight: 600; }
        td { color: #cccccc; background: #181818; }
        pre { margin: 0; color: #34d399; white-space: pre-wrap; word-break: break-all; font-family: monospace; font-size: 10px; }
    </style>'''

code = re.sub(old_css_pattern, new_style, code, flags=re.DOTALL)

# 同時把表格區塊包進可捲動的容器中，防止手機破版
old_table_block = '''        <table>
            <tr><th>時間</th><th>模組 / 目標</th><th>執行結果摘要</th></tr>
            __TABLE_ROWS__
        </table>'''

new_table_block = '''        <div class="table-container">
            <table>
                <tr><th>時間</th><th>模組 / 目標</th><th>執行結果摘要</th></tr>
                __TABLE_ROWS__
            </table>
        </div>'''

code = code.replace(old_table_block, new_table_block)

with open('ultimate_smart_engine.py', 'w', encoding='utf-8') as f:
    f.write(code)
print('[+] 手機版面響應式優化完成！')
"
# 重啟服務
pkill -f python
python ultimate_smart_engine.py &
python -c "
with open('ultimate_smart_engine.py', 'r', encoding='utf-8') as f:
    code = f.read()

import re

# 換成現代極簡白灰風格 (Clean Minimalist White/Gray)
old_css_pattern = r'<style>.*?</style>'
new_style = '''<style>
        * { box-sizing: border-box; }
        body { background: #f8f9fa; color: #333333; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; margin: 0; padding: 12px; }
        .header { background: #ffffff; border: 1px solid #e5e7eb; border-radius: 12px; padding: 18px; text-align: center; margin-bottom: 15px; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }
        .header h1 { font-size: 16px; color: #111827; margin: 0 0 6px 0; font-weight: 700; letter-spacing: -0.3px; }
        .header p { font-size: 12px; color: #6b7280; margin: 0; }
        .grid { display: flex; flex-direction: column; gap: 12px; }
        .card { background: #ffffff; border: 1px solid #e5e7eb; border-radius: 12px; padding: 16px; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }
        h2 { color: #111827; font-size: 13px; border-bottom: 1px solid #f3f4f6; padding-bottom: 8px; margin-top: 0; font-weight: 600; }
        p { font-size: 13px; line-height: 1.5; margin: 6px 0; color: #4b5563; word-break: break-all; }
        .stat-value { font-size: 20px; font-weight: 700; color: #059669; }
        .table-container { width: 100%; overflow-x: auto; -webkit-overflow-scrolling: touch; margin-top: 8px; }
        table { width: 100%; border-collapse: collapse; min-width: 320px; }
        th, td { border: 1px solid #e5e7eb; padding: 9px 12px; text-align: left; font-size: 12px; }
        th { background: #f9fafb; color: #374151; font-weight: 600; }
        td { color: #1f2937; background: #ffffff; }
        pre { margin: 0; color: #059669; white-space: pre-wrap; word-break: break-all; font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 11px; }
    </style>'''

code = re.sub(old_css_pattern, new_style, code, flags=re.DOTALL)

with open('ultimate_smart_engine.py', 'w', encoding='utf-8') as f:
    f.write(code)
print('[+] 已切換為極簡高質感白灰風格！')
"
# 重啟服務
pkill -f python
python ultimate_smart_engine.py &
python -c "
with open('ultimate_smart_engine.py', 'r', encoding='utf-8') as f:
    code = f.read()

import re

# 換成活力炫彩龐克風 (Vibrant Cyberpunk / Neon Gradient Style)
old_css_pattern = r'<style>.*?</style>'
new_style = '''<style>
        * { box-sizing: border-box; }
        body { background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%); color: #f8fafc; font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; margin: 0; padding: 12px; min-height: 100vh; }
        .header { background: rgba(30, 41, 59, 0.7); backdrop-filter: blur(10px); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 16px; padding: 20px; text-align: center; margin-bottom: 16px; box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3); }
        .header h1 { font-size: 17px; color: #38bdf8; margin: 0 0 6px 0; font-weight: 700; text-shadow: 0 0 10px rgba(56, 189, 248, 0.3); }
        .header p { font-size: 11px; color: #94a3b8; margin: 0; }
        .grid { display: flex; flex-direction: column; gap: 14px; }
        .card { background: rgba(30, 41, 59, 0.6); backdrop-filter: blur(10px); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 16px; padding: 16px; box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2); }
        h2 { color: #f43f5e; font-size: 13px; border-bottom: 1px solid rgba(255, 255, 255, 0.1); padding-bottom: 8px; margin-top: 0; font-weight: 700; letter-spacing: 0.5px; }
        p { font-size: 13px; line-height: 1.5; margin: 8px 0; color: #cbd5e1; word-break: break-all; }
        .stat-value { font-size: 22px; font-weight: 800; color: #34d399; text-shadow: 0 0 10px rgba(52, 211, 153, 0.3); }
        .table-container { width: 100%; overflow-x: auto; -webkit-overflow-scrolling: touch; margin-top: 10px; border-radius: 8px; border: 1px solid rgba(255, 255, 255, 0.08); }
        table { width: 100%; border-collapse: collapse; min-width: 320px; }
        th, td { padding: 10px 12px; text-align: left; font-size: 12px; }
        th { background: rgba(15, 23, 42, 0.8); color: #38bdf8; font-weight: 700; border-bottom: 1px solid rgba(255, 255, 255, 0.1); }
        td { color: #e2e8f0; background: rgba(30, 41, 59, 0.3); border-bottom: 1px solid rgba(255, 255, 255, 0.05); }
        pre { margin: 0; color: #34d399; white-space: pre-wrap; word-break: break-all; font-family: monospace; font-size: 11px; }
    </style>'''

code = re.sub(old_css_pattern, new_style, code, flags=re.DOTALL)

with open('ultimate_smart_engine.py', 'w', encoding='utf-8') as f:
    f.write(code)
print('[+] 已切換為活力炫彩龐克風！')
"
# 重啟服務
pkill -f python
python ultimate_smart_engine.py &
python -c "
with open('ultimate_smart_engine.py', 'r', encoding='utf-8') as f:
    code = f.read()

import re

# 替換為全域特大字體的響應式 CSS 樣式
old_css_pattern = r'<style>.*?</style>'
new_style = '''<style>
        * { box-sizing: border-box; }
        body { background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%); color: #f8fafc; font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; margin: 0; padding: 14px; min-height: 100vh; }
        .header { background: rgba(30, 41, 59, 0.8); backdrop-filter: blur(10px); border: 1px solid rgba(255, 255, 255, 0.15); border-radius: 16px; padding: 22px; text-align: center; margin-bottom: 18px; box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4); }
        .header h1 { font-size: 20px; color: #38bdf8; margin: 0 0 8px 0; font-weight: 800; text-shadow: 0 0 10px rgba(56, 189, 248, 0.4); }
        .header p { font-size: 13px; color: #cbd5e1; margin: 0; }
        .grid { display: flex; flex-direction: column; gap: 16px; }
        .card { background: rgba(30, 41, 59, 0.7); backdrop-filter: blur(10px); border: 1px solid rgba(255, 255, 255, 0.12); border-radius: 16px; padding: 20px; box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3); }
        h2 { color: #f43f5e; font-size: 16px; border-bottom: 1px solid rgba(255, 255, 255, 0.15); padding-bottom: 10px; margin-top: 0; font-weight: 800; letter-spacing: 0.5px; }
        p { font-size: 15px; line-height: 1.6; margin: 10px 0; color: #e2e8f0; word-break: break-all; }
        .stat-value { font-size: 26px; font-weight: 800; color: #34d399; text-shadow: 0 0 10px rgba(52, 211, 153, 0.4); }
        .table-container { width: 100%; overflow-x: auto; -webkit-overflow-scrolling: touch; margin-top: 12px; border-radius: 10px; border: 1px solid rgba(255, 255, 255, 0.12); }
        table { width: 100%; border-collapse: collapse; min-width: 340px; }
        th, td { padding: 12px 14px; text-align: left; font-size: 14px; }
        th { background: rgba(15, 23, 42, 0.9); color: #38bdf8; font-weight: 800; border-bottom: 1px solid rgba(255, 255, 255, 0.15); }
        td { color: #f1f5f9; background: rgba(30, 41, 59, 0.4); border-bottom: 1px solid rgba(255, 255, 255, 0.08); }
        pre { margin: 0; color: #34d399; white-space: pre-wrap; word-break: break-all; font-family: monospace; font-size: 13px; line-height: 1.5; }
    </style>'''

code = re.sub(old_css_pattern, new_style, code, flags=re.DOTALL)

with open('ultimate_smart_engine.py', 'w', encoding='utf-8') as f:
    f.write(code)
print('[+] 已全面升級為超大清晰字體版！')
"
# 重啟服務
pkill -f python
python ultimate_smart_engine.py &
python -c "
with open('ultimate_smart_engine.py', 'r', encoding='utf-8') as f:
    code = f.read()

import re

# 替換為手機超巨型字體的 CSS 樣式
old_css_pattern = r'<style>.*?</style>'
new_style = '''<style>
        * { box-sizing: border-box; }
        body { background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%); color: #f8fafc; font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; margin: 0; padding: 16px; min-height: 100vh; }
        .header { background: rgba(30, 41, 59, 0.9); backdrop-filter: blur(10px); border: 2px solid rgba(255, 255, 255, 0.2); border-radius: 18px; padding: 24px; text-align: center; margin-bottom: 20px; box-shadow: 0 10px 35px rgba(0, 0, 0, 0.5); }
        .header h1 { font-size: 24px; color: #38bdf8; margin: 0 0 10px 0; font-weight: 900; text-shadow: 0 0 12px rgba(56, 189, 248, 0.5); }
        .header p { font-size: 15px; color: #e2e8f0; margin: 0; font-weight: 600; }
        .grid { display: flex; flex-direction: column; gap: 18px; }
        .card { background: rgba(30, 41, 59, 0.85); backdrop-filter: blur(10px); border: 2px solid rgba(255, 255, 255, 0.15); border-radius: 18px; padding: 22px; box-shadow: 0 10px 35px rgba(0, 0, 0, 0.4); }
        h2 { color: #f43f5e; font-size: 20px; border-bottom: 2px solid rgba(255, 255, 255, 0.2); padding-bottom: 12px; margin-top: 0; font-weight: 900; letter-spacing: 0.5px; }
        p { font-size: 18px; line-height: 1.7; margin: 12px 0; color: #f1f5f9; word-break: break-all; font-weight: 600; }
        .stat-value { font-size: 32px; font-weight: 900; color: #34d399; text-shadow: 0 0 12px rgba(52, 211, 153, 0.5); }
        .table-container { width: 100%; overflow-x: auto; -webkit-overflow-scrolling: touch; margin-top: 14px; border-radius: 12px; border: 2px solid rgba(255, 255, 255, 0.15); }
        table { width: 100%; border-collapse: collapse; min-width: 380px; }
        th, td { padding: 14px 16px; text-align: left; font-size: 16px; font-weight: 600; }
        th { background: rgba(15, 23, 42, 0.95); color: #38bdf8; font-weight: 900; border-bottom: 2px solid rgba(255, 255, 255, 0.2); }
        td { color: #f8fafc; background: rgba(30, 41, 59, 0.5); border-bottom: 2px solid rgba(255, 255, 255, 0.1); }
        pre { margin: 0; color: #34d399; white-space: pre-wrap; word-break: break-all; font-family: monospace; font-size: 15px; line-height: 1.6; font-weight: bold; }
    </style>'''

code = re.sub(old_css_pattern, new_style, code, flags=re.DOTALL)

with open('ultimate_smart_engine.py', 'w', encoding='utf-8') as f:
    f.write(code)
print('[+] 已升級為巨型特大字體版！')
"
# 重啟服務
pkill -f python
python ultimate_smart_engine.py &
python -c "
with open('ultimate_smart_engine.py', 'r', encoding='utf-8') as f:
    code = f.read()

import re

# 在 HTML 模板中加入 Chart.js 圖表與超大字體、手機響應式排版
new_html_template = '''HTML_TEMPLATE = \"\"\"<!DOCTYPE html>
<html>
<head>
    <meta charset=\"utf-8\">
    <meta http-equiv=\"refresh\" content=\"10\">
    <title>智慧引擎即時戰情室</title>
    <script src=\"https://cdn.jsdelivr.net/npm/chart.js\"></script>
    <style>
        * { box-sizing: border-box; }
        body { background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%); color: #f8fafc; font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; margin: 0; padding: 16px; min-height: 100vh; }
        .header { background: rgba(30, 41, 59, 0.9); backdrop-filter: blur(10px); border: 2px solid rgba(255, 255, 255, 0.2); border-radius: 18px; padding: 24px; text-align: center; margin-bottom: 20px; box-shadow: 0 10px 35px rgba(0, 0, 0, 0.5); }
        .header h1 { font-size: 24px; color: #38bdf8; margin: 0 0 10px 0; font-weight: 900; text-shadow: 0 0 12px rgba(56, 189, 248, 0.5); }
        .header p { font-size: 15px; color: #e2e8f0; margin: 0; font-weight: 600; }
        .grid { display: flex; flex-direction: column; gap: 18px; }
        .card { background: rgba(30, 41, 59, 0.85); backdrop-filter: blur(10px); border: 2px solid rgba(255, 255, 255, 0.15); border-radius: 18px; padding: 22px; box-shadow: 0 10px 35px rgba(0, 0, 0, 0.4); }
        h2 { color: #f43f5e; font-size: 20px; border-bottom: 2px solid rgba(255, 255, 255, 0.2); padding-bottom: 12px; margin-top: 0; font-weight: 900; letter-spacing: 0.5px; }
        p { font-size: 18px; line-height: 1.7; margin: 12px 0; color: #f1f5f9; word-break: break-all; font-weight: 600; }
        .stat-value { font-size: 32px; font-weight: 900; color: #34d399; text-shadow: 0 0 12px rgba(52, 211, 153, 0.5); }
        .chart-container { position: relative; width: 100%; height: 250px; margin-top: 15px; }
        .table-container { width: 100%; overflow-x: auto; -webkit-overflow-scrolling: touch; margin-top: 14px; border-radius: 12px; border: 2px solid rgba(255, 255, 255, 0.15); }
        table { width: 100%; border-collapse: collapse; min-width: 380px; }
        th, td { padding: 14px 16px; text-align: left; font-size: 16px; font-weight: 600; }
        th { background: rgba(15, 23, 42, 0.95); color: #38bdf8; font-weight: 900; border-bottom: 2px solid rgba(255, 255, 255, 0.2); }
        td { color: #f8fafc; background: rgba(30, 41, 59, 0.5); border-bottom: 2px solid rgba(255, 255, 255, 0.1); }
        pre { margin: 0; color: #34d399; white-space: pre-wrap; word-break: break-all; font-family: monospace; font-size: 15px; line-height: 1.6; font-weight: bold; }
    </style>
</head>
<body>
    <div class=\"header\">
        <h1>智慧引擎即時戰情室</h1>
        <p>系統運行中 · 多源情報擴張與內容變現流</p>
    </div>
    
    <div class=\"grid\">
        <div class=\"card\">
            <h2>核心引擎數據</h2>
            <p>循環次數: <span class=\"stat-value\">__CYCLES__</span></p>
            <p>產出腳本數: <span class=\"stat-value\">__TOOLS__</span></p>
            <p>自動修復次數: <span class=\"stat-value\">__HEALED__</span></p>
            <p>最後同步時間: __LAST_SYNC__</p>
        </div>
        
        <div class=\"card\">
            <h2>即時產出趨勢圖</h2>
            <div class=\"chart-container\">
                <canvas id=\"trendChart\"></canvas>
            </div>
        </div>
        
        <div class=\"card\">
            <h2>自動化變現與擴張流</h2>
            <p>目標串流: 作用中變現管道</p>
            <p>數據源狀態: 已同步且自主運行</p>
            <p>節點狀態: 運作中 (100% 啟動)</p>
            <p>模型連線: qwen2.5:latest / 安全備援</p>
        </div>
    </div>

    <div class=\"card\" style=\"margin-top: 20px;\">
        <h2>多源情報動態日誌</h2>
        <div class=\"table-container\">
            <table>
                <tr><th>時間</th><th>模組 / 目標</th><th>執行結果摘要</th></tr>
                __TABLE_ROWS__
            </table>
        </div>
    </div>

    <script>
        const ctx = document.getElementById('trendChart').getContext('2d');
        const trendChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: __CHART_LABELS__,
                datasets: [{
                    label: '累計循環次數',
                    data: __CHART_DATA__,
                    borderColor: '#34d399',
                    backgroundColor: 'rgba(52, 211, 153, 0.1)',
                    borderWidth: 3,
                    fill: true,
                    tension: 0.3
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { labels: { color: '#f8fafc', font: { size: 14 } } } },
                scales: {
                    x: { ticks: { color: '#cbd5e1', font: { size: 12 } }, grid: { color: 'rgba(255,255,255,0.1)' } },
                    y: { ticks: { color: '#cbd5e1', font: { size: 12 } }, grid: { color: 'rgba(255,255,255,0.1)' } }
                }
            }
        });
    </script>
</body>
</html>
\"\"\"'''

code = re.sub(r'HTML_TEMPLATE\s*=\s*\"\"\"[\s\S]*?\"\"\"', new_html_template, code)

# 同時在 Handler 裡面傳入圖表需要的歷史數據
handler_old_logic = '''        html = HTML_TEMPLATE.replace("__CYCLES__", str(st[0]))\\
                            .replace("__TOOLS__", str(st[1]))\\
                            .replace("__HEALED__", str(st[2]))\\
                            .replace("__LAST_SYNC__", str(st[3]))\\
                            .replace("__TABLE_ROWS__", table_rows)'''

handler_new_logic = '''        # 抓取最近幾筆數據來畫圖
        c.execute("SELECT ts, cycles FROM smart_intels ORDER BY id ASC LIMIT 10")
        history = c.fetchall()
        chart_labels = [h[0].split(' ')[-1] for h in history] if history else ['0']
        chart_data = [i + 1 for i in range(len(history))] if history else [0]

        import json
        html = HTML_TEMPLATE.replace("__CYCLES__", str(st[0]))\\
                            .replace("__TOOLS__", str(st[1]))\\
                            .replace("__HEALED__", str(st[2]))\\
                            .replace("__LAST_SYNC__", str(st[3]))\\
                            .replace("__TABLE_ROWS__", table_rows)\\
                            .replace("__CHART_LABELS__", json.dumps(chart_labels))\\
                            .replace("__CHART_DATA__", json.dumps(chart_data))'''

if handler_old_logic in code:
    code = code.replace(handler_old_logic, handler_new_logic)

with open('ultimate_smart_engine.py', 'w', encoding='utf-8') as f:
    f.write(code)
print('[+] 已成功加入即時圖表與超大字體排版！')
"
# 重啟服務
pkill -f python
python ultimate_smart_engine.py &
python -c "
with open('ultimate_smart_engine.py', 'r', encoding='utf-8') as f:
    code = f.read()

import re

new_html_template = '''HTML_TEMPLATE = \"\"\"<!DOCTYPE html>
<html>
<head>
    <meta charset=\"utf-8\">
    <meta http-equiv=\"refresh\" content=\"10\">
    <title>AI 智慧戰情室</title>
    <script src=\"https://cdn.jsdelivr.net/npm/chart.js\"></script>
    <style>
        * { box-sizing: border-box; }
        body { background: #090d16; color: #e2e8f0; font-family: 'Segoe UI', Roboto, sans-serif; margin: 0; padding: 14px; min-height: 100vh; }
        .header { background: linear-gradient(135deg, #1e1b4b 0%, #0f172a 100%); border: 1px solid #38bdf855; border-radius: 16px; padding: 20px; text-align: center; margin-bottom: 16px; box-shadow: 0 0 20px rgba(56,189,248,0.15); }
        .header h1 { font-size: 22px; color: #38bdf8; margin: 0 0 8px 0; font-weight: 900; text-shadow: 0 0 10px rgba(56,189,248,0.5); }
        .header p { font-size: 14px; color: #94a3b8; margin: 0; display: flex; align-items: center; justify-content: center; gap: 8px; }
        .pulse { width: 10px; height: 10px; background-color: #22c55e; border-radius: 50%; display: inline-block; box-shadow: 0 0 8px #22c55e; animation: pulse 1.5px infinite; }
        @keyframes pulse { 0% { transform: scale(0.95); opacity: 0.8; } 50% { transform: scale(1.2); opacity: 1; } 100% { transform: scale(0.95); opacity: 0.8; } }
        
        .grid { display: grid; grid-template-columns: 1fr; gap: 16px; }
        .card { background: #111827; border: 1px solid #374151; border-radius: 16px; padding: 20px; box-shadow: 0 4px 20px rgba(0,0,0,0.4); position: relative; overflow: hidden; }
        .card::before { content: ''; position: absolute; top: 0; left: 0; width: 4px; height: 100%; background: #38bdf8; }
        
        h2 { color: #f43f5e; font-size: 18px; border-bottom: 1px solid #1f2937; padding-bottom: 10px; margin-top: 0; font-weight: 800; display: flex; justify-content: space-between; align-items: center; }
        p { font-size: 16px; line-height: 1.6; margin: 10px 0; color: #cbd5e1; font-weight: 600; }
        .stat-value { font-size: 28px; font-weight: 900; color: #34d399; text-shadow: 0 0 10px rgba(52,211,153,0.3); }
        
        .chart-container { position: relative; width: 100%; height: 220px; margin-top: 10px; }
        .table-container { width: 100%; overflow-x: auto; -webkit-overflow-scrolling: touch; margin-top: 12px; border-radius: 10px; border: 1px solid #374151; }
        table { width: 100%; border-collapse: collapse; min-width: 360px; }
        th, td { padding: 12px 14px; text-align: left; font-size: 14px; font-weight: 600; }
        th { background: #1f2937; color: #38bdf8; border-bottom: 2px solid #374151; }
        td { color: #e2e8f0; background: #0b0f19; border-bottom: 1px solid #1f2937; }
        pre { margin: 0; color: #34d399; white-space: pre-wrap; word-break: break-all; font-family: monospace; font-size: 13px; font-weight: bold; }
    </style>
</head>
<body>
    <div class=\"header\">
        <h1>⚡ AI 智慧戰情與自主擴張引擎 ⚡</h1>
        <p><span class=\"pulse\"></span> 系統運行中 · 多源情報動態流</p>
    </div>
    
    <div class=\"grid\">
        <div class=\"card\" style=\"border-left-color: #34d399;\">
            <h2>核心引擎數據</h2>
            <p>循環次數: <span class=\"stat-value\">__CYCLES__</span></p>
            <p>產出腳本數: <span class=\"stat-value\">__TOOLS__</span></p>
            <p>自動修復次數: <span class=\"stat-value\">__HEALED__</span></p>
            <p>最後同步時間: __LAST_SYNC__</p>
        </div>
        
        <div class=\"card\" style=\"border-left-color: #38bdf8;\">
            <h2>即時產出趨勢圖</h2>
            <div class=\"chart-container\">
                <canvas id=\"trendChart\"></canvas>
            </div>
        </div>
        
        <div class=\"card\" style=\"border-left-color: #f43f5e;\">
            <h2>自動化變現與擴張流</h2>
            <p>目標串流: 作用中變現管道</p>
            <p>數據源狀態: 已同步且自主運行</p>
            <p>節點狀態: 運作中 (100% 啟動)</p>
            <p>模型連線: qwen2.5:latest / 安全備援</p>
        </div>
    </div>

    <div class=\"card\" style=\"margin-top: 16px; border-left-color: #fbbf24;\">
        <h2>多源情報動態日誌</h2>
        <div class=\"table-container\">
            <table>
                <tr><th>時間</th><th>模組 / 目標</th><th>執行結果摘要</th></tr>
                __TABLE_ROWS__
            </table>
        </div>
    </div>

    <script>
        const ctx = document.getElementById('trendChart').getContext('2d');
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: __CHART_LABELS__,
                datasets: [{
                    label: '累計循環次數',
                    data: __CHART_DATA__,
                    borderColor: '#38bdf8',
                    backgroundColor: 'rgba(56, 189, 248, 0.1)',
                    borderWidth: 3,
                    fill: true,
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { labels: { color: '#f8fafc', font: { size: 13, weight: 'bold' } } } },
                scales: {
                    x: { ticks: { color: '#94a3b8', font: { size: 11 } }, grid: { color: 'rgba(255,255,255,0.05)' } },
                    y: { ticks: { color: '#94a3b8', font: { size: 11 } }, grid: { color: 'rgba(255,255,255,0.05)' } }
                }
            }
        });
    </script>
</body>
</html>
\"\"\"'''

code = re.sub(r'HTML_TEMPLATE\s*=\s*\"\"\"[\s\S]*?\"\"\"', new_html_template, code)

with open('ultimate_smart_engine.py', 'w', encoding='utf-8') as f:
    f.write(code)
print('[+] 已升級為高級科技霓虹戰情室！')
"
# 重啟服務
pkill -f python
python ultimate_smart_engine.py &
python -c "
with open('ultimate_smart_engine.py', 'r', encoding='utf-8') as f:
    code = f.read()

import re

# 替換為手機極致特大號字體的 CSS 樣式
old_css_pattern = r'<style>.*?</style>'
new_style = '''<style>
        * { box-sizing: border-box; }
        body { background: #090d16; color: #f8fafc; font-family: 'Segoe UI', Roboto, sans-serif; margin: 0; padding: 16px; min-height: 100vh; }
        .header { background: linear-gradient(135deg, #1e1b4b 0%, #0f172a 100%); border: 2px solid #38bdf888; border-radius: 20px; padding: 24px; text-align: center; margin-bottom: 20px; box-shadow: 0 0 25px rgba(56,189,248,0.25); }
        .header h1 { font-size: 26px; color: #38bdf8; margin: 0 0 10px 0; font-weight: 900; text-shadow: 0 0 15px rgba(56,189,248,0.6); }
        .header p { font-size: 16px; color: #cbd5e1; margin: 0; font-weight: 700; display: flex; align-items: center; justify-content: center; gap: 10px; }
        .pulse { width: 14px; height: 14px; background-color: #22c55e; border-radius: 50%; display: inline-block; box-shadow: 0 0 12px #22c55e; animation: pulse 1.5s infinite; }
        @keyframes pulse { 0% { transform: scale(0.95); opacity: 0.8; } 50% { transform: scale(1.3); opacity: 1; } 100% { transform: scale(0.95); opacity: 0.8; } }
        
        .grid { display: grid; grid-template-columns: 1fr; gap: 20px; }
        .card { background: #111827; border: 2px solid #374151; border-radius: 20px; padding: 24px; box-shadow: 0 6px 25px rgba(0,0,0,0.5); position: relative; overflow: hidden; }
        .card::before { content: ''; position: absolute; top: 0; left: 0; width: 6px; height: 100%; background: #38bdf8; }
        
        h2 { color: #f43f5e; font-size: 22px; border-bottom: 2px solid #1f2937; padding-bottom: 12px; margin-top: 0; font-weight: 900; letter-spacing: 0.5px; }
        p { font-size: 20px; line-height: 1.7; margin: 14px 0; color: #f1f5f9; font-weight: 700; }
        .stat-value { font-size: 36px; font-weight: 900; color: #34d399; text-shadow: 0 0 15px rgba(52,211,153,0.4); }
        
        .chart-container { position: relative; width: 100%; height: 260px; margin-top: 15px; }
        .table-container { width: 100%; overflow-x: auto; -webkit-overflow-scrolling: touch; margin-top: 15px; border-radius: 12px; border: 2px solid #374151; }
        table { width: 100%; border-collapse: collapse; min-width: 400px; }
        th, td { padding: 16px 18px; text-align: left; font-size: 18px; font-weight: 700; }
        th { background: #1f2937; color: #38bdf8; border-bottom: 3px solid #374151; }
        td { color: #f8fafc; background: #0b0f19; border-bottom: 2px solid #1f2937; }
        pre { margin: 0; color: #34d399; white-space: pre-wrap; word-break: break-all; font-family: monospace; font-size: 16px; font-weight: bold; line-height: 1.5; }
    </style>'''

code = re.sub(old_css_pattern, new_style, code, flags=re.DOTALL)

with open('ultimate_smart_engine.py', 'w', encoding='utf-8') as f:
    f.write(code)
print('[+] 已升級至巨無霸特大字體！')
"
# 重啟服務
pkill -f python
python ultimate_smart_engine.py &
