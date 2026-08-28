with open("server.py", "r", encoding="utf-8") as f:
    code = f.read()

# 替換為支援手機響應式的 HTML 模板
mobile_html_patch = '''@app.route('/')
def dashboard():
    return """
    <!DOCTYPE html>
    <html lang="zh-Hant">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>天網行動指揮中心</title>
        <style>
            * { box-sizing: border-box; }
            body { background-color: #090d16; color: #f8fafc; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, monospace; padding: 12px; margin: 0; }
            h1 { color: #38bdf8; border-bottom: 2px solid #1e293b; padding-bottom: 8px; font-size: 1.2rem; margin-top: 5px; }
            .status-bar { background: #1e293b; padding: 8px 12px; border-radius: 6px; font-size: 0.85rem; margin-bottom: 12px; color: #34d399; }
            .grid { display: flex; flex-direction: column; gap: 10px; }
            .card { background: #111827; border: 1px solid #1f2937; border-radius: 8px; padding: 12px; }
            .card h3 { margin: 0 0 6px 0; color: #38bdf8; font-size: 0.95rem; }
            .card p { margin: 4px 0; font-size: 0.82rem; color: #94a3b8; }
            .badge { background: #0369a1; color: #e0f2fe; padding: 2px 6px; border-radius: 4px; font-size: 0.75rem; float: right; }
        </style>
    </head>
    <body>
        <h1>⚡ 天網行動指揮中心</h1>
        <div class="status-bar">
            系統狀態：<strong>16 核心全線運轉中</strong>
        </div>
        
        <div class="grid">
            <div class="card">
                <h3>🏛️ 多 Agent 委員會 <span class="badge">已激活</span></h3>
                <p>架構、資安、爬蟲與主編分工協作中</p>
            </div>
            <div class="card">
                <h3>🛡️ 零信任與抗量子 <span class="badge">ML-KEM</span></h3>
                <p>晶格密碼學通道防護啟動</p>
            </div>
            <div class="card">
                <h3>🌐 分散式 Raft 共識 <span class="badge">LEADER</span></h3>
                <p>多節點日誌對齊與防腦裂</p>
            </div>
            <div class="card">
                <h3>💰 Web3 自主資金流 <span class="badge">追蹤中</span></h3>
                <p>金庫地址：0xSkynetTreasury</p>
            </div>
            <div class="card">
                <h3>🧠 RAG 向量長期記憶 <span class="badge">正常</span></h3>
                <p>fusion_hub_vector.db 索引中</p>
            </div>
            <div class="card">
                <h3>⚙️ Android 硬體調度 <span class="badge">Nice -5</span></h3>
                <p>背景行程優先級最佳化</p>
            </div>
        </div>
    </body>
    </html>
    """'''

# 更新路由
if "@app.route('/')" in code:
    parts = code.split("@app.route('/')")
    code = parts[0] + mobile_html_patch
    with open("server.py", "w", encoding="utf-8") as f:
        f.write(code)
    print("Successfully updated to Mobile-Optimized UI!")
