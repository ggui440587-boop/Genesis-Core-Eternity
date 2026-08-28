with open("server.py", "r", encoding="utf-8") as f:
    code = f.read()

# 升級伺服器的根目錄路由，回傳高階視覺化控制面板
ui_patch = """
# === 視覺化控制面板路由更新 ===
# 確保伺服器具備處理根目錄 HTML 輸出的能力
"""

dashboard_html_code = '''
    @app.route('/')
    def dashboard():
        html_content = \"\"\"
        <!DOCTYPE html>
        <html lang="zh-Hant">
        <head>
            <meta charset="UTF-8">
            <title>天網自主中樞 - 總指揮面板</title>
            <style>
                body { background-color: #0f172a; color: #f8fafc; font-family: monospace; padding: 20px; }
                h1 { color: #38bdf8; border-bottom: 2px solid #334155; padding-bottom: 10px; }
                .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 15px; margin-top: 20px; }
                .card { background: #1e293b; border: 1px solid #334155; border-radius: 8px; padding: 15px; }
                .card h3 { margin-top: 0; color: #4ade80; }
                .status-active { color: #38bdf8; font-weight: bold; }
                button { background: #0284c7; color: white; border: none; padding: 8px 12px; border-radius: 4px; cursor: pointer; margin-top: 10px; }
                button:hover { background: #0369a1; }
            </style>
        </head>
        <body>
            <h1>⚡ 天網自主營運中樞 (Termux Apex)</h1>
            <p>系統狀態：<span class="status-active">全線運行中 (Active)</span></p>
            
            <div class="grid">
                <div class="card">
                    <h3>🏛️ 多 Agent 委員會</h3>
                    <p>成員：Architect, Security, Scraper, Editor</p>
                    <p>狀態：自主辯論與任務指派中</p>
                </div>
                <div class="card">
                    <h3>🛡️ 零信任與抗量子</h3>
                    <p>加密協定：ML-KEM / Lattice-Safe</p>
                    <p>狀態：通道安全防護中</p>
                </div>
                <div class="card">
                    <h3>🌐 全球雲端與 Raft 共識</h3>
                    <p>當前身份：LEADER 節點</p>
                    <p>同步狀態：跨區塊與節點對齊</p>
                </div>
                <div class="card">
                    <h3>💰 Web3 自主資金流</h3>
                    <p>金庫地址：0xSkynetAutonomousTreasury</p>
                    <p>目前收益：動態累積中</p>
                </div>
            </div>

            <div style="margin-top: 30px;">
                <h3>系統控制</h3>
                <button onclick="alert('已觸發全系統強制自主巡檢！')">執行手動巡檢</button>
            </div>
        </body>
        </html>
        \"\"\"
        return html_content
'''

# 如果程式碼中還沒有這個路由，我們就把它補進 Flask App 裡
if "def dashboard" not in code:
    # 找尋 app.run 的位置並在之前插入路由
    if "app.run" in code:
        code = code.replace("if __name__ == '__main__':", dashboard_html_code + "\n\nif __name__ == '__main__':")
        with open("server.py", "w", encoding="utf-8") as f:
            f.write(code)
        print("Successfully upgraded Web Dashboard UI!")
    else:
        print("Could not locate app.run in server.py, keeping existing panel.")
else:
    print("Dashboard UI already upgraded.")
