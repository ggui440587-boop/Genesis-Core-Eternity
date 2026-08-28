import os
import urllib.request
import json
import datetime
import subprocess

class UltimateGlobalFusion:
    def __init__(self, output_dir="ultimate_hub"):
        self.output_dir = output_dir
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def fetch_and_fuse(self, name, url):
        print(f"-> 🌐 正在融合全球專案: {name}")
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=10) as response:
                source_code = response.read().decode('utf-8')
            
            file_path = os.path.join(self.output_dir, f"{name.lower()}_ultimate.py")
            
            fused_content = (
                f"# -*- coding: utf-8 -*-\n"
                f"# 終極融合模組: {name}\n"
                f"# 融合時間: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
                f"# === 原始碼開端 ===\n"
                f"{source_code}\n"
                f"# === 原始碼結尾 ===\n"
            )
            
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(fused_content)
                
            print(f"-> ✅ 成功寫入檔案: {file_path}")
            return file_path
        except Exception as e:
            print(f"-> ❌ 融合失敗 [{name}]: {e}")
            return None

    def verify_syntax(self, file_path):
        try:
            subprocess.run(
                ["python", "-m", "py_compile", file_path],
                capture_output=True,
                text=True,
                check=True,
                timeout=5
            )
            print(f"-> 🎉 語法檢驗通過: {file_path}")
            return True
        except Exception as e:
            print(f"-> ⚠️ 語法檢驗異常: {e}")
            return False

if __name__ == "__main__":
    print("【全景模組終極融合器啟動】\n")
    
    fusion = UltimateGlobalFusion()
    
    # 核心精選專案
    targets = [
        {"name": "Requests", "url": "https://raw.githubusercontent.com/psf/requests/refs/heads/main/src/requests/__init__.py"},
        {"name": "FastAPI", "url": "https://raw.githubusercontent.com/fastapi/fastapi/refs/heads/master/fastapi/__init__.py"},
        {"name": "Rich", "url": "https://raw.githubusercontent.com/Textualize/rich/refs/heads/main/rich/__init__.py"}
    ]
    
    for item in targets:
        path = fusion.fetch_and_fuse(item["name"], item["url"])
        if path:
            fusion.verify_syntax(path)
        print("-" * 30)
        
    print("\n-> ✨ 所有專案終極融合流程執行完畢！")
