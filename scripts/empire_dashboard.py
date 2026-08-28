import os
import subprocess
from datetime import datetime

def show_dashboard():
    os.system('clear' if os.name == 'posix' else 'cls')
    print("==================================================")
    print(" 🛡️  帝國戰情面板 (Empire Command Dashboard) 🛡️ ")
    print("==================================================")
    print(f"[*] 當前時間：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 50)
    print(" [背景常駐進程狀態 (Python Processes)]")
    
    # 檢查背景中的 python 執行緒
    result = subprocess.run("ps aux | grep python | grep -v grep", shell=True, capture_output=True, text=True)
    if result.stdout.strip():
        print(result.stdout.strip())
    else:
        print(" [!] 目前沒有偵測到運行中的背景 Python 進程。")
        
    print("==================================================")
    print(" 提示：輸入 'python scripts/empire_dashboard.py' 即可隨時重新整理面板！")
    print("==================================================")

if __name__ == "__main__":
    show_dashboard()

