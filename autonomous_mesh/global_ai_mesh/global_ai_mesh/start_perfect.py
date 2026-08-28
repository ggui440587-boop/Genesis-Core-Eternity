import subprocess
import time
import os

print("==========================================")
print("🚀 正在啟動 100% 完美的完全體系統...")
print("==========================================")

# 確保主伺服器運行
if not os.path.exists("server.py"):
    print("錯誤: 找不到 server.py，請確認檔案是否存在。")
    exit(1)

server_proc = subprocess.Popen(["python", "server.py"])
time.sleep(2)

# 啟動 Watchdog 守護行程
if os.path.exists("watchdog.sh"):
    subprocess.Popen(["./watchdog.sh"])

# 啟動 Cloudflare 公網穿透隧道
print("正在建立安全公網隧道 (Cloudflare Tunnel)...")
try:
    tunnel_proc = subprocess.Popen(["cloudflared", "tunnel", "--url", "http://127.0.0.1:8081"], 
                                   stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    
    # 嘗試捕捉並顯示公網連結
    for line in tunnel_proc.stdout:
        if "trycloudflare.com" in line:
            print("\n✨ 【完美的雲端公網網址已生成！】")
            print(line.strip())
            print("==========================================")
            break
except Exception as e:
    print(f"Cloudflare 啟動提示: {e} (本地端 http://127.0.0.1:8081 仍可正常訪問)")

# 保持主行程
try:
    server_proc.wait()
except KeyboardInterrupt:
    print("正在安全關閉系統...")
    server_proc.terminate()
