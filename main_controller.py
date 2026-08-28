import time
import asyncio
from rich.console import Console
from config_plugin import ConfigPlugin
from worker_plugin import WorkerPlugin
from database_plugin import DatabasePlugin
from git_plugin import GitPlugin
from heartbeat_plugin import HeartbeatPlugin
from memory_plugin import MemoryPlugin
from crypto_plugin import CryptoPlugin
from network_plugin import NetworkPlugin
from background_plugin import BackupPlugin
from benchmark_plugin import BenchmarkPlugin
from cli_plugin import CLIPlugin
from guard_plugin import GuardPlugin
from dashboard_plugin import DashboardPlugin
from notification_plugin import NotificationPlugin
from partner_plugin import PartnerPlugin
from search_plugin import SearchPlugin
from hardware_plugin import HardwarePlugin
from analytics_plugin import AnalyticsPlugin
from scheduler_plugin import SchedulerPlugin
from cache_plugin import CacheCleanerPlugin
from report_plugin import ReportPlugin

console = Console()

class MainController:
    def __init__(self):
        self.config = ConfigPlugin()
        self.cli = CLIPlugin()
        self.partner = PartnerPlugin()
        
        self.version = f"{self.config.get('version')}-Docosinonary-Matrix"
        
        # 載入所有二十二大外掛
        self.worker = WorkerPlugin()
        self.db = DatabasePlugin()
        self.git = GitPlugin()
        self.heartbeat = HeartbeatPlugin()
        self.memory = MemoryPlugin()
        self.crypto = CryptoPlugin()
        self.network = NetworkPlugin(endpoint_url=self.config.get('remote_endpoint'))
        self.backup = BackupPlugin()
        self.benchmark = BenchmarkPlugin()
        self.guard = GuardPlugin()
        self.dashboard = DashboardPlugin()
        self.notification = NotificationPlugin()
        self.search = SearchPlugin()
        self.hardware = HardwarePlugin()
        self.analytics = AnalyticsPlugin()
        self.scheduler = SchedulerPlugin(default_delay=self.config.get('sleep_interval'))
        self.cache_cleaner = CacheCleanerPlugin()
        self.reporter = ReportPlugin()
        self.task_counter = 0

        # 啟動網頁儀表板伺服器
        self.dashboard.start_server()
        self.partner.introduce()

    async def run_cycle(self):
        self.task_counter += 1
        current_time = self.scheduler.get_timestamp()
        console.print(f"[green]-> 🚀 主控制器觸發二十二大外掛完全體循環 (版本: {self.version}) | 時間: {current_time}[/green]")
        
        # 0. 開始計時
        self.benchmark.start_timer()
        
        # 0a. 心跳檢測
        self.heartbeat.pulse()
        
        # 0b. 記憶體防護檢查
        self.memory.check_memory()
        
        # 0c. 硬體與電池狀態檢查
        battery = self.hardware.get_battery_status()
        console.print(f"-> 🔋 [硬體外掛] 電池電量: {battery.get('percentage')}% | 狀態: {battery.get('status')}")
        
        # 0d. 快取自動清理檢查
        if self.task_counter % 5 == 0:
            self.cache_cleaner.clean_cache()
        
        # 0e. 資料加密測試
        secure_token = self.crypto.encrypt_data(f"Report-Token-{self.task_counter}")
        
        # 0f. 網路通訊回報 (結合例外防護)
        @self.guard.auto_retry(max_retries=self.config.get('max_retries'), delay=1)
        def safe_network_call():
            return self.network.send_ping({"task_id": self.task_counter, "token": secure_token})
        safe_network_call()
        
        # 0g. 日誌備份檢查
        self.backup.archive_logs()
        
        # 0h. 產出執行報告
        self.reporter.generate_report(self.task_counter, "SUCCESS", f"Battery: {battery.get('percentage')}%")
        
        # 0i. 數據分析統計回報
        if self.task_counter % 3 == 0:
            stats = self.analytics.analyze_stats()
            console.print(f"-> 📊 [分析外掛] 系統統計 -> 總任務數: {stats['total_tasks']} | 成功率: {stats['success_rate']}")
        
        # 1. 執行背景任務
        await self.worker.execute_task(self.task_counter)
        
        # 2. 寫入資料庫紀錄
        self.db.save_log(self.task_counter, "SUCCESS")
        
        # 3. 執行 Git 自動同步
        self.git.sync_to_github()
        
        # 4. 結束計時
        self.benchmark.stop_timer(f"Task-{self.task_counter}")

if __name__ == "__main__":
    controller = MainController()
    try:
        console.print(f"[cyan]-> 💡 啟動二十二大外掛終極完全體系統，按 Ctrl + C 可安全終止。[/cyan]")
        while True:
            asyncio.run(controller.run_cycle())
            # 使用排程外掛進行動態暫停控制
            controller.scheduler.intelligent_sleep(controller.task_counter)
    except KeyboardInterrupt:
        console.print("[red]-> 🛑 模組化主控制器已被使用者手動終止。[/red]")
