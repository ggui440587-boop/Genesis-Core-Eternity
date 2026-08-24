import os
import sys
import sqlite3
import subprocess
import time
import questionary
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

class MatrixUltimateOS:
    def __init__(self, db_name="matrix_intel.db"):
        self.db_name = db_name

    def notify_user(self, message):
        """呼叫 Termux API 發出語音合成與震動通知"""
        try:
            # 震動手機
            subprocess.run("termux-vibrate -d 500", shell=True, capture_output=True)
            # 語音播報（如果手機裝有 Termux:API App）
            subprocess.run(f"termux-tts-speak '{message}'", shell=True, capture_output=True)
        except Exception:
            pass

    def backup_to_github(self):
        """自動將本地智庫與報表打包推送到私人 GitHub 倉庫備份"""
        console.print("[yellow]🔄 正在將數位帝國智庫同步至 GitHub 雲端...[/yellow]")
        try:
            subprocess.run("git add matrix_intel.db intelligence_vault.md generated_posts.md", shell=True, capture_output=True)
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
            commit_msg = f"Auto-backup Matrix Vault: {timestamp}"
            subprocess.run(f'git commit -m "{commit_msg}"', shell=True, capture_output=True)
            result = subprocess.run("git push origin main", shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                console.print("[bold green]✅ GitHub 雲端備份成功！帝國數據安全無虞。[/bold green]")
                self.notify_user("智庫已成功備份至雲端")
            else:
                console.print("[yellow]⚠️ Git 推送略過（可能需檢查遠端分支或無新變更）。[/yellow]")
        except Exception as e:
            console.print(f"[red]❌ 備份發生異常: {e}[/red]")

    def show_dashboard(self):
        """展示 Rich 動態戰情看板"""
        if not os.path.exists(self.db_name):
            console.print("[red]尚未建立資料庫，請先執行情報搜集！[/red]")
            return

        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM intel_vault")
        total_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT category, COUNT(*) FROM intel_vault GROUP BY category")
        category_stats = cursor.fetchall()
        
        cursor.execute("SELECT source, title, category FROM intel_vault ORDER BY id DESC LIMIT 6")
        recent_items = cursor.fetchall()
        conn.close()

        console.clear()
        console.print(Panel.fit("[bold cyan]🚀 楊哲熙的 Termux 數位自動化作戰矩陣 - 終端作業系統[/bold cyan]", border_style="bright_blue"))
        
        table = Table(title="📊 智庫總覽", border_style="green")
        table.add_column("總情報數", justify="center", style="bold magenta")
        for cat, _ in category_stats:
            table.add_column(cat, justify="center", style="cyan")
        table.add_row(str(total_count), *[str(c) for _, c in category_stats])
        console.print(table)

        item_table = Table(title="🔥 最新戰利品", border_style="yellow")
        item_table.add_column("分類", style="cyan", width=16)
        item_table.add_column("標題", style="white", width=50)
        for _, title, cat in recent_items:
            item_table.add_row(cat, title[:45] + "...")
        console.print(item_table)
        input("\n按下 Enter 鍵返回主選單...")

    def run_pipeline(self):
        """執行全套情報挖掘與內容生成"""
        console.print("[yellow]⚙️ 正在執行全自動情報煉金術...[/yellow]")
        try:
            subprocess.run(["python", "deep_diver.py"], check=True)
            subprocess.run(["python", "matrix_factory.py"], check=True)
            console.print("[bold green]✨ 煉金完畢！情報與短影音腳本已全數更新。[/bold green]")
            self.notify_user("情報煉金已完成")
        except Exception as e:
            console.print(f"[red]❌ 執行失敗: {e}[/red]")
        input("\n按下 Enter 鍵返回主選單...")

    def search_vault(self):
        """互動式智慧檢索"""
        keyword = questionary.text("請輸入您想在智庫中搜尋的關鍵字（例如 AI, Bitcoin, Claude）：").ask()
        if not keyword:
            return
        
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT title, link, category FROM intel_vault WHERE title LIKE ? OR category LIKE ?", (f"%{keyword}%", f"%{keyword}%"))
        results = cursor.fetchall()
        conn.close()

        console.print(f"\n[bold yellow]🔍 檢索結果（關鍵字：{keyword}）：[/bold yellow]\n")
        if not results:
            console.print("[red]沒有找到相符的標的。[/red]")
        else:
            for idx, (title, link, cat) in enumerate(results, 1):
                console.print(f"{idx}. [{cat}] {title}\n   通道: {link}\n")
        input("\n按下 Enter 鍵返回主選單...")

    def main_menu(self):
        """主選單互動迴圈"""
        while True:
            console.clear()
            console.print(Panel.fit("[bold green]🔮 矩陣作業系統主控台 (Matrix OS)[/bold green]", border_style="green"))
            
            choice = questionary.select(
                "請選擇您要執行的賽博龐克模組：",
                choices=[
                    "📈 1. 檢視動態戰情看板",
                    "⚙️ 2. 手動執行情報挖掘與工廠煉金",
                    "🔍 3. 智庫智慧關鍵字檢索",
                    "☁️ 4. Git 雲端防護網同步備份",
                    "🚪 5. 退出至命令列"
                ]
            ).ask()

            if "1" in choice:
                self.show_dashboard()
            elif "2" in choice:
                self.run_pipeline()
            elif "3" in choice:
                self.search_vault()
            elif "4" in choice:
                self.backup_to_github()
                input("\n按下 Enter 鍵返回主選單...")
            elif "5" in choice:
                console.print("[cyan]期待再次啟動矩陣。再見，大師！[/cyan]")
                break

if __name__ == "__main__":
    os_system = MatrixUltimateOS()
    os_system.main_menu()

