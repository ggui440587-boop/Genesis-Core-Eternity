import os
import urllib.request
import json
import datetime
import logging
import subprocess
import time

# 初始化系統日誌
logging.basicConfig(
    filename="system.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    encoding="utf-8"
)

class AutoDaemonGlobalFusionFactory:
    def __init__(self, output_dir="manufacturing_hub", db_file="production_database.json"):
        self.output_dir = output_dir
        self.db_file = db_file
        self._setup_factory()

    def _setup_factory(self):
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
            logging.info(f"建立生產資料夾: {self.output_dir}")

    def fetch_source_code(self, url, retries=3, delay=2):
        print(f"-> 🌍 [自動守護採購] 正在下載原始碼: {url}")
        for attempt in range(1, retries + 1):
            try:
                req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req, timeout=10) as response:
                    code_content = response.read().decode('utf-8')
                print("-> ✅ 原始碼下載成功。")
                return code_content
            except Exception as e:
                print(f"-> ⚠️ 下載失敗 (嘗試 {attempt}/{retries}): {str(e)}")
                if attempt < retries:
                    time.sleep(delay)
                else:
                    logging.error(f"全球原始碼下載最終失敗: {url}")
        return None

    def fuse_and_produce(self, module_name, external_code):
        print(f"-> 🧪 [深度融合] 正在將全球開源碼熔鑄至本地模組: {module_name}")
        file_path = os.path.join(self.output_dir, f"{module_name.lower()}_auto_fused.py")
        safe_code = external_code if external_code else "# No code"

        fused_program = (
            "# -*- coding: utf-8 -*-\n"
            "# --------------------------------------------------\n"
            f"# 自動守護開源融合模組: {module_name}\n"
            f"# 產出時間: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            "# --------------------------------------------------\n\n"
            "# === [全球開源原始碼開始] ===\n"
            f"{safe_code}\n"
            "# === [全球開源原始碼結束] ===\n\n"
            "def auto_module_hook():\n"
            "    print('-> 🚀 [本地驗證] 自動守護模組運行正常！')\n"
            "    return True\n\n"
            "if __name__ == '__main__':\n"
            "    auto_module_hook()\n"
        )

        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(fused_program)
            print(f"-> 💾 寫入硬碟成功: {file_path}")
            return file_path
        except Exception as e:
            print(f"-> ❌ 寫入失敗: {str(e)}")
            return None

    def test_and_record(self, file_path, module_name, source_url):
        print(f"-> 🔍 [品質檢驗] 檢查模組語法: {file_path}")
        status = "FAILED"
        code_size = 0
        try:
            if os.path.exists(file_path):
                code_size = os.path.getsize(file_path)

            subprocess.run(
                ["python", "-m", "py_compile", file_path],
                capture_output=True,
                text=True,
                check=True,
                timeout=10
            )
            print("-> 🎉 語法檢驗完美通過！")
            status = "SUCCESS"
        except Exception as e:
            print(f"-> ⚠️ 檢驗失敗: {e}")

        metrics = {"file_size_bytes": code_size}
        self._save_to_database(module_name, file_path, source_url, status, metrics)

    def _save_to_database(self, module_name, file_path, source_url, status, metrics):
        record = {
            "product_name": module_name,
            "file_path": file_path,
            "source_url": source_url,
            "status": status,
            "metrics": metrics,
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        dataset = []
        if os.path.exists(self.db_file):
            try:
                with open(self.db_file, "r", encoding="utf-8") as f:
                    dataset = json.load(f)
            except Exception:
                pass
        dataset.append(record)
        with open(self.db_file, "w", encoding="utf-8") as f:
            json.dump(dataset, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    print("【全自動循環守護工廠啟動】")
    print("-> 💡 提示：按 Ctrl + C 可以隨時終止背景守護。\n")
    
    factory = AutoDaemonGlobalFusionFactory()
    
    sources = [
        {"name": "RequestsAuto", "url": "https://raw.githubusercontent.com/psf/requests/refs/heads/main/src/requests/__init__.py"},
        {"name": "FastAPIAuto", "url": "https://raw.githubusercontent.com/fastapi/fastapi/refs/heads/master/fastapi/__init__.py"},
        {"name": "FlaskAuto", "url": "https://raw.githubusercontent.com/pallets/flask/refs/heads/main/src/flask/__init__.py"},
        {"name": "ClickAuto", "url": "https://raw.githubusercontent.com/pallets/click/refs/heads/main/src/click/__init__.py"},
        {"name": "RichAuto", "url": "https://raw.githubusercontent.com/Textualize/rich/refs/heads/main/rich/__init__.py"},
        {"name": "PydanticAuto", "url": "https://raw.githubusercontent.com/pydantic/pydantic/refs/heads/main/pydantic/__init__.py"}
    ]
    
    # 設定自動循環間隔（單位：秒），例如每 300 秒（5分鐘）自動抓取一次，或改為 10 秒測試
    interval_seconds = 30
    
    try:
        while True:
            print(f"\n[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] -> 🔄 開始新一輪全球開源專案自動巡航...")
            for item in sources:
                print("=" * 40)
                code = factory.fetch_source_code(item["url"])
                if code:
                    path = factory.fuse_and_produce(item["name"], code)
                    if path:
                        factory.test_and_record(path, item["name"], item["url"])
            
            print(f"\n-> 💤 本輪巡航完畢。進入自動休眠，等待 {interval_seconds} 秒後進行下一輪...")
            time.sleep(interval_seconds)
            
    except KeyboardInterrupt:
        print("\n-> 🛑 使用者手動終止，自動守護工廠已安全關閉。")
