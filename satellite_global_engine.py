import sqlite3
import time
import requests
import random
import os
import threading
import importlib.util
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

DB_FILE = "satellite_global.db"
PORT = 5050
MODULES_DIR = "orbital_modules"

def init_environment():
    if not os.path.exists(MODULES_DIR):
        os.makedirs(MODULES_DIR)
    
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS core_status (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            orbit_syncs INT DEFAULT 0,
            active_modules INT DEFAULT 0,
            telemetry_success INT DEFAULT 0,
            last_sync DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS global_intels (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sector TEXT,
            target_node TEXT,
            telemetry_data TEXT,
            status TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute("SELECT COUNT(*) FROM core_status")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO core_status (orbit_syncs, active_modules, telemetry_success) VALUES (0, 0, 0)")
    
    conn.commit()
    conn.close()

def satellite_global_cycle():
    init_environment()
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # 選擇全球跑透透或衛星軌道來源
    sector = random.choice(['GLOBAL_ISS_TRACKER', 'GLOBAL_WEATHER_SATELLITE', 'GLOBAL_VESSEL_TRACKER'])
    target_node = ""
    telemetry_data = ""
    module_filename = ""
    module_code = ""

    if sector == 'GLOBAL_ISS_TRACKER':
        # 追蹤真實的國際太空站 (ISS) 即時位置
        url = "http://api.open-notify.org/iss-now.json"
        try:
            res = requests.get(url, timeout=5)
            if res.status_code == 200:
                data = res.json()
                position = data.get('iss_position', {})
                lat = position.get('latitude', '0')
                lon = position.get('longitude', '0')
                target_node = "ISS-Orbit-Station"
                telemetry_data = f"Lat: {lat}, Lon: {lon} (Orbital Altitude: ~400km)"
                
                module_filename = os.path.join(MODULES_DIR, "mod_space_iss.py")
                module_code = f'''# Orbital Module: ISS Tracker
def run_telemetry():
    print("[ORBIT] Tracking ISS at Lat: {lat}, Lon: {lon}")
    return {{"status": "SUCCESS", "lat": "{lat}", "lon": "{lon}"}}
'''
            else:
                telemetry_data = f"ISS API status {res.status_code}"
        except Exception as e:
            telemetry_data = f"ISS connection error: {str(e)[:30]}"

    elif sector == 'GLOBAL_WEATHER_SATELLITE':
        # 抓取全球開源氣象與地表數據 (以 NOAA / 自由氣象 API 為例)
        url = "https://api.weather.gov/points/37.7749,-122.4194" # 範例點位
        try:
            res = requests.get(url, headers={"User-Agent": "GlobalSatelliteCore/1.0"}, timeout=5)
            if res.status_code == 200:
                props = res.json().get('properties', {})
                grid_id = props.get('gridId', 'UNKNOWN')
                target_node = f"NOAA-Weather-Grid-{grid_id}"
                telemetry_data = f"Global Grid Sync Successful. Radar Station: {grid_id}"
                
                module_filename = os.path.join(MODULES_DIR, f"mod_weather_{grid_id}.py")
                module_code = f'''# Orbital Module: Weather Grid {grid_id}
def run_telemetry():
    print("[GRID] Processing atmospheric telemetry for grid {grid_id}")
    return {{"status": "SUCCESS", "grid": "{grid_id}"}}
'''
            else:
                telemetry_data = f"Weather API status {res.status_code}"
        except Exception as e:
            telemetry_data = f"Weather connection error: {str(e)[:30]}"

    else:
        # 全球開源衛星/海洋節點模擬追蹤
        target_node = "Global-OSINT-Node-Alpha"
        telemetry_data = "Global mesh node synchronized across terrestrial boundaries."
        module_filename = os.path.join(MODULES_DIR, "mod_mesh_alpha.py")
        module_code = '''# Orbital Module: Mesh Alpha
def run_telemetry():
    print("[MESH] Global terrestrial node active.")
    return {"status": "SUCCESS"}
'''

    status_flag = "SUCCESS" if module_filename else "WARNING"
    cursor.execute("INSERT INTO global_intels (sector, target_node, telemetry_data, status) VALUES (?, ?, ?, ?)",
                   (sector, target_node or 'Global-Node', telemetry_data, status_flag))

    success_inc = 0
    if module_filename and module_code:
        with open(module_filename, 'w', encoding='utf-8') as f:
            f.write(module_code)
        
        try:
            mod_name = os.path.basename(module_filename)[:-3]
            spec = importlib.util.spec_from_file_location(mod_name, module_filename)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            if hasattr(mod, 'run_telemetry'):
                res_dict = mod.run_telemetry()
                if res_dict.get('status') == 'SUCCESS':
                    success_inc = 1
        except Exception as ex:
            print(f"[Telemetry Dispatch Error] {ex}")

    active_files = [f for f in os.listdir(MODULES_DIR) if f.endswith('.py')] if os.path.exists(MODULES_DIR) else []

    cursor.execute("""
        UPDATE core_status 
        SET orbit_syncs = orbit_syncs + 1, 
            active_modules = ?, 
            telemetry_success = telemetry_success + ?, 
            last_sync = CURRENT_TIMESTAMP 
        WHERE id = 1
    """, (len(active_files), success_inc))

    conn.commit()
    conn.close()

def background_loop():
    init_environment()
    while True:
        satellite_global_cycle()
        time.sleep(20)

class SatelliteHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == '/action':
            query = parse_qs(parsed.query)
            cmd = query.get('cmd', [''])[0]
            conn = sqlite3.connect(DB_FILE)
            cursor = conn.cursor()
            if cmd == 'trigger':
                satellite_global_cycle()
            elif cmd == 'purge':
                cursor.execute("DELETE FROM global_intels")
                cursor.execute("UPDATE core_status SET orbit_syncs=0, active_modules=0, telemetry_success=0 WHERE id=1")
                conn.commit()
                for f in os.listdir(MODULES_DIR):
                    if f.endswith('.py'):
                        os.remove(os.path.join(MODULES_DIR, f))
            conn.close()
            self.send_response(303)
            self.send_header('Location', '/')
            self.end_headers()
            return

        if parsed.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()

            conn = sqlite3.connect(DB_FILE)
            cursor = conn.cursor()

            cursor.execute("SELECT orbit_syncs, active_modules, telemetry_success, last_sync FROM core_status WHERE id = 1")
            status = cursor.fetchone() or (0, 0, 0, '-')

            active_files = [f for f in os.listdir(MODULES_DIR) if f.endswith('.py')] if os.path.exists(MODULES_DIR) else []

            cursor.execute("SELECT sector, target_node, telemetry_data, status, timestamp FROM global_intels ORDER BY id DESC LIMIT 6")
            intels = cursor.fetchall()

            conn.close()

            html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <title>GLOBAL & SATELLITE TELEMETRY CORE</title>
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <meta http-equiv="refresh" content="5">
                <style>
                    body {{
                        background: #020408;
                        color: #00ffff;
                        font-family: monospace;
                        padding: 12px;
                        margin: 0;
                        font-size: 12px;
                    }}
                    h1 {{
                        color: #00ff66;
                        text-align: center;
                        font-size: 15px;
                        border-bottom: 1px solid #00ffff33;
                        padding-bottom: 8px;
                        text-shadow: 0 0 8px #00ff66;
                    }}
                    .grid {{
                        display: grid;
                        grid-template-columns: 1fr 1fr;
                        gap: 8px;
                        margin-bottom: 10px;
                    }}
                    .box {{
                        background: #08111e;
                        border: 1px solid #00ffff44;
                        padding: 8px;
                        text-align: center;
                        border-radius: 6px;
                    }}
                    .controls {{
                        display: flex;
                        gap: 8px;
                        margin-bottom: 12px;
                    }}
                    .btn {{
                        flex: 1;
                        background: #003333;
                        color: #00ffff;
                        border: 1px solid #00ffff;
                        padding: 8px;
                        text-align: center;
                        text-decoration: none;
                        font-weight: bold;
                        border-radius: 6px;
                    }}
                    .btn-danger {{ background: #330000; border-color: #ff3366; color: #ff3366; }}
                    .card {{
                        background: #08111e;
                        border: 1px solid #00ffff44;
                        padding: 10px;
                        margin-bottom: 10px;
                        border-radius: 6px;
                    }}
                    h2 {{
                        color: #ff9900;
                        font-size: 11px;
                        border-bottom: 1px dashed #00ffff44;
                        padding-bottom: 4px;
                        margin: 0 0 8px 0;
                    }}
                    .row {{
                        background: #020408;
                        border-left: 3px solid #00ff66;
                        padding: 6px;
                        margin-bottom: 6px;
                        font-size: 10px;
                        display: flex;
                        justify-content: space-between;
                        align-items: center;
                    }}
                    .row.warning {{ border-left-color: #ff3366; }}
                </style>
            </head>
            <body>
                <h1>🛰️ 全球跑透透與衛星軌道情資中樞</h1>
                <div style="text-align:center; color: #88a; font-size:9px; margin-bottom:10px;">ORBITAL SYNC TIME: {status[3]}</div>

                <div class="grid">
                    <div class="box">全球軌道同步次數<br><b style="color:#00ff66; font-size:14px;">{status[0]}</b></div>
                    <div class="box">現役軌道模組<br><b style="color:#00ffff; font-size:14px;">{status[1]} 個</b></div>
                    <div class="box" style="grid-column: span 2;">遙感調度成功率: <b style="color:#ff9900;">{status[2]} 次</b></div>
                </div>

                <div class="controls">
                    <a class="btn" href="/action?cmd=trigger">⚡ 手動同步衛星與全球節點</a>
                    <a class="btn btn-danger" href="/action?cmd=purge">🗑️ 清空軌道數據與模組</a>
                </div>

                <div class="card">
                    <h2>📂 軌道模組實體庫 (<code>{MODULES_DIR}/</code>)</h2>
                    <div style="font-size:10px; color:#aaa; max-height:70px; overflow-y:auto; background:#020408; padding:6px; border:1px solid #00ffff22;">
                        {', '.join(active_files) if active_files else '暫無軌道模組'}
                    </div>
                </div>

                <div class="card">
                    <h2>📡 全球即時遙感與衛星回傳日誌</h2>
                    {''.join(f'''
                    <div class="row {"warning" if i[3]=="WARNING" else ""}">
                        <div>
                            <span style="color:{"#ff3366" if i[3]=="WARNING" else "#00ff66"};">[{i[0]}]</span> 
                            <b>{i[1]}</b><br>
                            <span style="color:#88a; font-size:9px;">{i[2]}</span>
                        </div>
                        <div style="text-align:right;">
                            <span style="font-size:9px; color:#00ffff;">{i[3]}</span>
                        </div>
                    </div>
                    ''' for i in intels) if intels else '<div style="color:#88a; text-align:center;">等待衛星與全球信號接入...</div>'}
                </div>
            </body>
            </html>
            """
            self.wfile.write(html.encode('utf-8'))

def run_server():
    server = HTTPServer(('127.0.0.1', PORT), SatelliteHandler)
    print(f"[*] 全球與衛星遙感核心已啟動: http://127.0.0.1:{PORT}")
    server.serve_forever()

if __name__ == '__main__':
    t = threading.Thread(target=background_loop, daemon=True)
    t.start()
    run_server()
