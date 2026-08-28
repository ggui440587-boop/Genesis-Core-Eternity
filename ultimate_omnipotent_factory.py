import os
import json
import urllib.request
import datetime
import subprocess
import sqlite3
import time
import shutil

class UltimateOmnipotentFactory:
    def __init__(self, output_file="genesis_core_eternity.py", db_file="fusion_history.db", backup_dir="backup"):
        self.output_file = output_file
        self.db_file = db_file
        self.backup_dir = backup_dir
        self.sources_file = "sources.json"
        self._init_environment()

    def _init_environment(self):
        if not os.path.exists(self.backup_dir):
            os.makedirs(self.backup_dir)
        
        # 初始化 SQLite 資料庫
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

    def _backup_existing_core(self):
        if os.path.exists(self.output_file):
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = os.path.join(self.backup_dir, f"genesis_core_{timestamp}.py")
            shutil.copy(self.output_file, backup_path)
            print(f"-> 📦 已自動備份舊核心至: {backup_path}")

    def load_sources(self):
        if not os.path.exists(self.sources_file):
            print(f"-> ⚠️ 找不到 {self.sources_file}，使用預設清單。")
            return [
                {"name": "Requests", "url": "https://raw.githubusercontent.com/psf/requests/refs/heads/main/src/requests/__init__.py"}
            ]
        try:
            with open(self.sources_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"-> ❌ 載入設定檔失敗: {e}")
            return []

    def run_fusion_cycle(self):
        print(f"\n[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] -> 🚀 開始全功能融合循環...")
        
        # 1. 備份舊核心
        self._backup_existing_core()
        
        sources = self.load_sources()
        genetic_pool = []

        for gene in sources:
            name = gene.get("name")
            url = gene.get("url")
            print(f"-> 🧬 正在融合基因: {name}")
            try:
                req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req, timeout=8) as response:
                    code_content = response.read().decode('utf-8')
                clean_code = f"\n# === [GENE START: {name}] ===\n" + code_content + f"\n# === [GENE END: {name}] ===\n"
                genetic_pool.append(clean_code)
                print(f"-> ✅ 成功: {name}")
            except Exception as e:
                print(f"-> ⚠️ 異常（已自動相容略過） [{name}]: {e}")
                fallback_code = f"\n# === [GENE FALLBACK: {name}] ===\n# Status: Offline\n"
                genetic_pool.append(fallback_code)

        # 2. 合成永恆核心
        header = (
            "# -*- coding: utf-8 -*-\n"
            "# ==================================================\n"
            "# 專案名稱: Genesis-Core-Eternity (全功能終極永恆核心)\n"
            f"# 最後合成時間: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            "# ==================================================\n\n"
        )
        body = "".join(genetic_pool)
        footer = (
            "\n\ndef ultimate_core_hook():\n"
            "    print('-> 🚀 全功能永恆核心運作正常！')\n"
            "    return True\n\n"
            "if __name__ == '__main__':\n"
            "    ultimate_core_hook()\n"
        )

        full_code = header + body + footer
        status = "SUCCESS"

        try:
            with open(self.output_file, "w", encoding="utf-8") as f:
                f.write(full_code)
            print(f"-> 💾 核心寫入成功: {self.output_file}")
        except Exception as e:
            print(f"-> ❌ 寫入失敗: {e}")
            status = "FAILED"

        # 3. 語法檢驗與統計分析
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
            print("📊 [終極融合工廠綜合統計報告]")
            print("=" * 40)
            print(f"• 總行數: {total_lines} 行 (程式碼: {code_lines} 行)")
            print(f"• 兼容基因片段數: {gene_count} 個")
            print(f"• 狀態: {status}")
            print("=" * 40 + "\n")

        # 4. 寫入 SQLite 資料庫持久化紀錄
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO fusion_logs (timestamp, total_lines, code_lines, gene_count, status) VALUES (?, ?, ?, ?, ?)",
            (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), total_lines, code_lines, gene_count, status)
        )
        conn.commit()
        conn.close()

if __name__ == "__main__":
    factory = UltimateOmnipotentFactory()
    
    # 可選擇單次執行或啟動背景排程循環
    # 這裡預設執行單次，若需背景常駐排程可改用 while 迴圈
    factory.run_fusion_cycle()
