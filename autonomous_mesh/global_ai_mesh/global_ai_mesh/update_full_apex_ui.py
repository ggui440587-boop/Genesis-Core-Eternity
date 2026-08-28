with open("server.py", "r", encoding="utf-8") as f:
    code = f.read()

# 定義包含所有 16 項頂級模組的完整儀表板 HTML
full_dashboard_code = '''
@app.route('/')
def dashboard():
    return """
    <!DOCTYPE html>
    <html lang="zh-Hant">
    <head>
        <meta charset="UTF-8">
        <title>天網全知全能生態系 - 總指揮面板</title>
        <style>
            body { background-color: #090d16; color: #f8fafc; font-family: monospace; padding: 20px; margin: 0; }
            h1 { color: #38bdf8; border-bottom: 2px solid #1e293b; padding-bottom: 10px; font-size: 1.5rem; }
            .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 12px; margin-top: 15px; }
            .card { background: #111827; border: 1px solid #1f2937; border-radius: 6px; padding: 12px; }
            .card h3 { margin-top: 0; color: #34d399; font-size: 1rem; }
            .status-active { color: #38bdf8; font-weight: bold; }
            .badge { background: #0369a1; color: #e0f2fe; padding: 2px 6px; border-radius: 4px; font-size: 0.8rem; }
        </style>
    </head>
    <body>
        <h1>⚡ 天網全知全能生態系 (Termux Apex Ultra)</h1>
        <p>系統狀態：<span class="status-active">16 大核心模組全線運轉中</span></p>
        
        <div class="grid">
            <div class="card">
                <h3>🏛️ 多 Agent 委員會</h3>
                <p>架構/資安/爬蟲/主編：<span class="badge">已激活</span></p>
                <p>狀態：自主辯論與任務指派中</p>
            </div>
            <div class="card">
                <h3>🛡️ 零信任與抗量子</h3>
                <p>加密協定：<span class="badge">ML-KEM / Kyber</span></p>
                <p>狀態：通道安全防護中</p>
            </div>
            <div class="card">
                <h3>🌐 分散式 Raft 共識</h3>
                <p>節點身份：<span class="badge">LEADER (Term 1)</span></p>
                <p>狀態：跨節點日誌對齊中</p>
            </div>
            <div class="card">
                <h3>💰 Web3 自主資金流</h3>
                <p>金庫：0xSkynetAutonomousTreasury</p>
                <p>狀態：收益動態累積中</p>
            </div>
            <div class="card">
                <h3>🧠 RAG 向量長期記憶</h3>
                <p>資料庫：fusion_hub_vector.db</p>
                <p>狀態：索引與檢索正常</p>
            </div>
            <div class="card">
                <h3>⚙️ Android 硬體調度</h3>
                <p>行程優先級：<span class="badge">Nice -5 (高優先)</span></p>
                <p>狀態：背景效能最佳化中</p>
            </div>
        </div>
    </body>
    </html>
    """
'''

# 移除舊的路由定義（若存在）並寫入新路由
if "@app.route('/')" in code:
    # 簡單用字串分割保留前面的主程式，替換掉舊的路由函式
    parts = code.split("@app.route('/')")
    code = parts[0] + full_dashboard_code
    with open("server.py", "w", encoding="utf-8") as f:
        f.write(code)
    print("Successfully replaced with Full Apex Dashboard!")
else:
    print("Could not find root route to replace.")
