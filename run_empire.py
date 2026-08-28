import time
import subprocess
from datetime import datetime

def main():
    print("==================================================")
    print(" 👑 啟動帝國全息自動化與多源情報擴張總控中心（背景常駐版） 👑 ")
    print("==================================================")
    
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"[*] 啟動時間：{now}")
    
    scripts = [
        "scripts/auto_content_publisher.py",
        "scripts/micro_service_api.py",
        "scripts/telegram_affiliate_bot.py"
    ]
    
    for script in scripts:
        print(f"[-] 正在將模組送入背景常駐運行：{script}")
        # 使用 nohup 與 & 讓腳本在背景持續運行，輸出導向 /dev/null 保持乾淨
        subprocess.Popen(f"nohup python {script} > /dev/null 2>&1 &", shell=True)
        time.sleep(1)
            
    print("==================================================")
    print(" 🚀 所有引擎已成功常駐背景，全天候守護帝國！")
    print("==================================================")

if __name__ == "__main__":
    main()

