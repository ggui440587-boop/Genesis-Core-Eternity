import sqlite3
from datetime import datetime

try:
    from fastapi import FastAPI
    from fastapi.responses import HTMLResponse
    import uvicorn
except ImportError:
    # 若尚未安裝 FastAPI 則提示安裝
    import os
    os.system("pip install fastapi uvicorn > /dev/null 2>&1")
    from fastapi import FastAPI
    from fastapi.responses import HTMLResponse
    import uvicorn

app = FastAPI()
DB_NAME = "fusion_hub.db"

@app.get("/", response_class=HTMLResponse)
def read_root():
    gold, citizens, slaves = 0, 0, 0
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT SUM(quantity) FROM imperial_treasury")
        res_g = cursor.fetchone()
        gold = res_g[0] if res_g and res_g[0] else 0
        
        cursor.execute("SELECT SUM(citizens_count), SUM(slaves_count) FROM empire_domains")
        res_p = cursor.fetchone()
        if res_p:
            citizens = res_p[0] or 0
            slaves = res_p[1] or 0
        conn.close()
    except Exception:
        pass

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>👑 帝國全息御前大殿</title>
        <meta http-equiv="refresh" content="5">
        <style>
            body {{ background-color: #121212; color: #e0e0e0; font-family: monospace; text-align: center; padding: 50px; }}
            .card {{ background: #1e1e1e; border: 2px solid #333; padding: 20px; margin: 20px auto; width: 60%; border-radius: 10px; }}
            h1 {{ color: #ffd700; }}
            .metric {{ font-size: 24px; color: #00ffcc; }}
        </style>
    </head>
    <body>
        <h1>👑 數位帝國全息網頁大殿</h1>
        <p>即時監控中 (每 5 秒自動重新整理)</p>
        <div class="card">
            <h3>🪙 帝國資產與人口</h3>
            <p class="metric">金庫金幣：{gold}</p>
            <p class="metric">自由民：{citizens} 人 | 奴隸：{slaves} 人</p>
        </div>
        <p>🕒 當前時間：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)

