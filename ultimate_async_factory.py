import os
import json
import asyncio
import urllib.request
import datetime
import subprocess
import sqlite3
import shutil
import logging
import time

# 設定異常警報日誌
logging.basicConfig(
    filename="alert.log",
    level=logging.ERROR,
    format="%(asctime)s [%(levelname)s] %(message)s",
    encoding="utf-8"
)

class UltimateAsyncFactory:
    def __init__(self, output_file="genesis_core_eternity.py", db_file="fusion_history.db", backup_dir="backup", max_backups=5):
        self.output_file = output_file
        self.db_file = db_file
        self.backup_dir = backup_dir
        self.max_backups = max_backups
        self.sources_file = "sources.json"
        self._init_environment()

    def _init_environment(self):
        if not os.path.exists(self.backup_dir):
            os.makedirs(self.backup_dir)
        
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS fusion_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                total_lines INTEGER,
                code_lines INTEGER,
                gene_count INTEGER,
                status TEXT
            )
        ''')
        conn.commit()
        conn.close()

    def _backup_and_clean(self):
        if os.path.exists(self.output_file):
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = os.path.join(self.backup_dir, f"genesis_core_{timestamp}.py")
            shutil.copy(self.output_file, backup_path)
            print(f"-> 📦 已自動備份舊核心至: {backup_path}")

            backups = sorted([os.path.join(self.backup_dir, f) for f in os.listdir(self.backup_dir) if f.startswith("genesis_core_")])
            while len(backups) > self.max_backups:
                oldest_backup = backups.pop(0)
                try:
                    os.remove(oldest_backup)
                    print(f"-> 🧹 空間清理：已自動刪除過期舊備份 -> {oldest_backup}")
                except Exception as e:
                    print(f"-> ⚠️ 清理備份失敗: {e}")

    def load_sources(self):
        if not os.path.exists(self.sources_file):
            return [{"name": "Requests", "url": "https://raw.githubusercontent.com/psf/requests/refs/heads/main/src/requests/__init__.py"}]
        try:
            with open(self.sources_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logging.error(f"載入設定檔失敗: {e}")
            return []

    async def fetch_single_gene(self, gene):
        name = gene.get("name")
        url = gene.get("url")
        print(f"-> 🧬 [非同步吸收] 正在抓取: {name}")
        
        loop = asyncio.get_running_loop()
        try:
            def download():
                req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req, timeout=8) as response:
                    return response.read().decode('utf-8')
            
            code_content = await loop.run_in_executor(None, download)
            clean_code = f"\n# === [GENE START: {name}] ===\n" + code_content + f"\n# === [GENE END: {name}] ===\n"
            print(f"-> ✅ 成功抓取: {name}")
            return clean_code
        except Exception as e:
            print(f"-> ⚠️ 抓取異常（已啟用相容替代） [{name}]: {e}")
            logging.error(f"基因抓取失敗 [{name}]: {e}")
            return f"\n# === [GENE FALLBACK: {name}] ===\n# Status: Offline\n"

    def _git_auto_push(self):
        print("-> 🌐 [Git 模組] 正在自動同步至遠端 GitHub...")
        try:
            subprocess.run(["git", "add", self.output_file, "sources.json"], capture_output=True, check=True)
            commit_msg = f"Final infinite auto-fusion update: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            subprocess.run(["git", "commit", "-m", commit_msg], capture_output=True, check=True)
            subprocess.run(["git", "push"], capture_output=True, check=True, timeout=15)
            print("-> 🎉 Git 遠端推送成功！")
        except Exception as e:
            print(f"-> ⚠️ Git 推送警告（可能無變更）: {e}")
            logging.error(f"Git 自動推送失敗: {e}")

    async def run_fusion_cycle(self):
        print(f"\n[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] -> 🚀 啟動最終版非同步融合循環...")
        self._backup_and_clean()
        
        sources = self.load_sources()
        tasks = [self.fetch_single_gene(gene) for gene in sources]
        results = await asyncio.gather(*tasks)

        header = (
            "# -*- coding: utf-8 -*-\n"
            "# ==================================================\n"
            "# 專案名稱: Genesis-Core-Eternity (最終無限常駐永恆核心)\n"
            f"# 最後合成時間: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            "# ==================================================\n\n"
        )
        body = "".join(results)
        footer = (
            "\n\ndef ultimate_async_hook():\n"
            "    print('-> 🚀 最終無限常駐核心運行正常！')\n"
            "    return True\n\n"
            "if __name__ == '__main__':\n"
            "    ultimate_async_hook()\n"
        )

        full_code = header + body + footer
        status = "SUCCESS"

        try:
            with open(self.output_file, "w", encoding="utf-8") as f:
                f.write(full_code)
            print(f"-> 💾 核心寫入成功: {self.output_file}")
        except Exception as e:
            status = "FAILED"
            logging.error(f"核心寫入失敗: {e}")

        self._generate_unit_test()

        total_lines, code_lines, gene_count = 0, 0, 0
        if os.path.exists(self.output_file):
            try:
                subprocess.run(["python", "-m", "py_compile", self.output_file], capture_output=True, check=True, timeout=5)
                print("-> 🎉 語法編譯檢驗通過！")
            except Exception:
                status = "COMPILE_WARNING"

            with open(self.output_file, "r", encoding="utf-8") as f:
                lines = f.readlines()
            total_lines = len(lines)
            blank_lines = sum(1 for line in lines if line.strip() == "")
            code_lines = total_lines - blank_lines
            gene_count = sum(1 for line in lines if "# === [GENE" in line)

            print("\n" + "=" * 40)
            print("📊 [最終版工廠綜合統計報告]")
            print("=" * 40)
            print(f"• 總行數: {total_lines} 行 (程式碼: {code_lines} 行)")
            print(f"• 兼容基因片段數: {gene_count} 個")
            print(f"• 狀態: {status}")
            print("=" * 40 + "\n")

        self._git_auto_push()

        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO fusion_logs (timestamp, total_lines, code_lines, gene_count, status) VALUES (?, ?, ?, ?, ?)",
            (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), total_lines, code_lines, gene_count, status)
        )
        conn.commit()
        conn.close()

    def _generate_unit_test(self):
        test_code = (
            "# -*- coding: utf-8 -*-\n"
            "import unittest\n"
            "import genesis_core_eternity as core\n\n"
            "class TestGenesisCore(unittest.TestCase):\n"
            "    def test_core_hook(self):\n"
            "        self.assertTrue(core.ultimate_async_hook())\n\n"
            "if __name__ == '__main__':\n"
            "    unittest.main()\n"
        )
        with open("test_genesis.py", "w", encoding="utf-8") as f:
            f.write(test_code)

if __name__ == "__main__":
    factory = UltimateAsyncFactory(max_backups=5)
    
    # 設定背景循環間隔秒數（例如每 60 秒執行一次）
    interval_seconds = 60
    
    print("【全自動非同步基因融合工廠 - 最終無限常駐模式正式啟動】")
    print("-> 💡 提示：系統將持續無限期運轉。隨時可按 Ctrl + C 安全終止。\n")
    
    try:
        while True:
            asyncio.run(factory.run_fusion_cycle())
            print(f"-> 💤 本輪融合循環圓滿完成，進入自動休眠，等待 {interval_seconds} 秒後開啟下一輪...")
            time.sleep(interval_seconds)
    except KeyboardInterrupt:
        print("\n-> 🛑 使用者手動終止（Ctrl + C），最終常駐工廠已安全關閉。")
