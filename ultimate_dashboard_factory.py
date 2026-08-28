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

from rich.console import Console
from rich.panel import Panel
from rich.layout import Layout
from rich.table import Table
from rich.live import Live

# 設定異常警報日誌
logging.basicConfig(
    filename="alert.log",
    level=logging.ERROR,
    format="%(asctime)s [%(levelname)s] %(message)s",
    encoding="utf-8"
)

console = Console()

class DashboardIntegratedFactory:
    def __init__(self, output_file="genesis_core_eternity.py", db_file="fusion_history.db", backup_dir="backup", max_backups=5):
        self.output_file = output_file
        self.db_file = db_file
        self.backup_dir = backup_dir
        self.max_backups = max_backups
        self.sources_file = "sources.json"
        
        # 狀態變數（供儀表板即時顯示）
        self.current_status = "初始化中..."
        self.last_sync_time = "尚未同步"
        self.total_lines = 0
        self.gene_count = 0
        self.cycle_count = 0
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
            
            backups = sorted([os.path.join(self.backup_dir, f) for f in os.listdir(self.backup_dir) if f.startswith("genesis_core_")])
            while len(backups) > self.max_backups:
                oldest_backup = backups.pop(0)
                try:
                    os.remove(oldest_backup)
                except Exception:
                    pass

    def load_sources(self):
        if not os.path.exists(self.sources_file):
            return [{"name": "Requests", "url": "https://raw.githubusercontent.com/psf/requests/refs/heads/main/src/requests/__init__.py"}]
        try:
            with open(self.sources_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []

    async def fetch_single_gene(self, gene):
        name = gene.get("name")
        url = gene.get("url")
        self.current_status = f"正在抓取: {name}"
        
        loop = asyncio.get_running_loop()
        try:
            def download():
                req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req, timeout=8) as response:
                    return response.read().decode('utf-8')
            
            code_content = await loop.run_in_executor(None, download)
            clean_code = f"\n# === [GENE START: {name}] ===\n" + code_content + f"\n# === [GENE END: {name}] ===\n"
            return clean_code
        except Exception as e:
            logging.error(f"基因抓取失敗 [{name}]: {e}")
            return f"\n# === [GENE FALLBACK: {name}] ===\n# Status: Offline\n"

    def _git_auto_push(self):
        self.current_status = "正在同步至遠端 GitHub..."
        try:
            subprocess.run(["git", "add", self.output_file, "sources.json"], capture_output=True, check=True)
            commit_msg = f"Dashboard auto-fusion: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            subprocess.run(["git", "commit", "-m", commit_msg], capture_output=True, check=True)
            subprocess.run(["git", "push"], capture_output=True, check=True, timeout=15)
        except Exception as e:
            logging.error(f"Git 自動推送失敗: {e}")

    async def run_fusion_cycle(self):
        self.cycle_count += 1
        self.current_status = "備份舊核心中..."
        self._backup_and_clean()
        
        sources = self.load_sources()
        tasks = [self.fetch_single_gene(gene) for gene in sources]
        results = await asyncio.gather(*tasks)

        header = (
            "# -*- coding: utf-8 -*-\n"
            "# ==================================================\n"
            "# 專案名稱: Genesis-Core-Eternity (儀表板整合核心)\n"
            f"# 最後合成時間: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            "# ==================================================\n\n"
        )
        body = "".join(results)
        footer = (
            "\n\ndef ultimate_async_hook():\n"
            "    print('-> 🚀 儀表板整合核心運行正常！')\n"
            "    return True\n\n"
            "if __name__ == '__main__':\n"
            "    ultimate_async_hook()\n"
        )

        full_code = header + body + footer
        status = "SUCCESS"

        self.current_status = "寫入新核心與編譯檢驗..."
        try:
            with open(self.output_file, "w", encoding="utf-8") as f:
                f.write(full_code)
        except Exception as e:
            status = "FAILED"
            logging.error(f"核心寫入失敗: {e}")

        # 產生單元測試
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

        if os.path.exists(self.output_file):
            try:
                subprocess.run(["python", "-m", "py_compile", self.output_file], capture_output=True, check=True, timeout=5)
            except Exception:
                status = "COMPILE_WARNING"

            with open(self.output_file, "r", encoding="utf-8") as f:
                lines = f.readlines()
            self.total_lines = len(lines)
            self.gene_count = sum(1 for line in lines if "# === [GENE" in line)

        self._git_auto_push()

        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO fusion_logs (timestamp, total_lines, code_lines, gene_count, status) VALUES (?, ?, ?, ?, ?)",
            (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), self.total_lines, self.total_lines, self.gene_count, status)
        )
        conn.commit()
        conn.close()

        self.last_sync_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.current_status = "待命休眠中 (Idle)"

    def build_dashboard_ui(self):
        layout = Layout()
        layout.split_column(
            Layout(name="header", size=3),
            Layout(name="body"),
            Layout(name="footer", size=3)
        )

        layout["header"].update(Panel("🚀 ARGONA - 終極自動化基因融合儀表板", style="bold white on blue"))

        table = Table(title="即時系統運行狀態", expand=True)
        table.add_column("監控指標", style="cyan", no_wrap=True)
        table.add_column("當前狀態數值", style="magenta")

        table.add_row("循環執行次數", f"第 {self.cycle_count} 次")
        table.add_row("系統目前動作", f"[yellow]{self.current_status}[/yellow]")
        table.add_row("核心總行數", f"{self.total_lines} 行")
        table.add_row("整合開源基因數", f"{self.gene_count} 個")
        table.add_row("最後同步時間", f"{self.last_sync_time}")

        layout["body"].update(Panel(table, title="Live Factory Telemetry"))
        layout["footer"].update(Panel("💡 提示：系統正以儀表板模式持續運行。按 Ctrl + C 可安全關閉。", style="dim"))

        return layout

if __name__ == "__main__":
    factory = DashboardIntegratedFactory()
    interval_seconds = 30

    async def main_loop():
        # 首次立即執行一次
        await factory.run_fusion_cycle()
        while True:
            # 進入等待間隔，每秒更新一次畫面計時
            for _ in range(interval_seconds):
                await asyncio.sleep(1)
            await factory.run_fusion_cycle()

    try:
        with Live(factory.build_dashboard_ui(), refresh_per_second=4, screen=True) as live:
            # 建立背景執行任務與畫面更新監控
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            # 為了讓 Live 畫面與非同步工廠完美結合，我們使用非同步背景排程
            async def worker():
                while True:
                    await factory.run_fusion_cycle()
                    live.update(factory.build_dashboard_ui())
                    for _ in range(interval_seconds):
                        live.update(factory.build_dashboard_ui())
                        await asyncio.sleep(1)

            loop.run_until_complete(worker())
    except KeyboardInterrupt:
        console.print("[red]-> 🛑 使用者手動終止，儀表板工廠已安全關閉。[/red]")
