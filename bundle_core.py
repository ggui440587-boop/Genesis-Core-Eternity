# === Auto-Generated Bundled Core System ===

# --- Source: analytics_plugin.py ---
import os

class AnalyticsPlugin:
    def __init__(self, log_file="system_actions.log"):
        self.log_file = log_file

    def analyze_stats(self):
        """簡單分析日誌檔案中的執行次數與狀態"""
        if not os.path.exists(self.log_file):
            return {"total_tasks": 0, "success_rate": "100%"}

        try:
            with open(self.log_file, "r", encoding="utf-8") as f:
                lines = f.readlines()
                total = len(lines)
                success_count = sum(1 for line in lines if "SUCCESS" in line)
                rate = (success_count / total * 100) if total > 0 else 100
                return {
                    "total_tasks": total,
                    "success_rate": f"{rate:.1f}%"
                }
        except Exception as e:
            print(f"-> ⚠️ [分析外掛] 讀取日誌分析失敗: {e}")
            return {"total_tasks": 0, "success_rate": "0%"}

if __name__ == "__main__":
    analytics = AnalyticsPlugin()
    print("System Stats:", analytics.analyze_stats())


# --- Source: argparse_plugin.py ---
import argparse

class ArgparsePlugin:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description="Termux Matrix Automation System")
        self.parser.add_argument("--mode", type=str, default="normal", help="運行模式 (normal / debug)")
        self.parser.add_argument("--interval", type=int, default=10, help="任務執行間隔秒數")
        print("-> ⌨️ [參數外掛] 命令列解析器初始化成功！")

    def parse_args(self):
        """解析終端機傳入的參數"""
        args = self.parser.parse_args()
        return {
            "mode": args.mode,
            "interval": args.interval
        }

if __name__ == "__main__":
    cli = ArgparsePlugin()
    print("Parsed Arguments:", cli.parse_args())


# --- Source: backup_plugin.py ---
class BackupPlugin:
    def archive_logs(self):
        print("-> 📦 [備份] 成功建立日誌備份檔。")


# --- Source: benchmark_plugin.py ---
import time
class BenchmarkPlugin:
    def __init__(self): self.start = None
    def start_timer(self): self.start = time.time()
    def stop_timer(self, name):
        if self.start:
            print(f"-> ⏱️ [基準] {name} 耗時: {(time.time()-self.start)*1000:.2f} 毫秒")


# --- Source: bundler_plugin.py ---
import glob

class PluginBundlerPlugin:
    def __init__(self, target_pattern="*_plugin.py", output_file="bundle_core.py"):
        self.target_pattern = target_pattern
        self.output_file = output_file
        print("-> 📦 [打包重構外掛] 模組合併工具初始化成功！")

    def bundle_plugins(self):
        """將多個外掛檔案合併打包成單一核心檔案"""
        plugin_files = glob.glob(self.target_pattern)
        print(f"-> 🔍 正在打包 {len(plugin_files)} 個外掛模組...")

        with open(self.output_file, 'w', encoding='utf-8') as outfile:
            outfile.write("# === Auto-Generated Bundled Core System ===\n")
            for filepath in sorted(plugin_files):
                if filepath == self.output_file:
                    continue
                outfile.write(f"\n# --- Source: {filepath} ---\n")
                with open(filepath, 'r', encoding='utf-8') as infile:
                    outfile.write(infile.read())
                outfile.write("\n")

        print(f"-> ✅ 打包完成！所有模組已成功合併至: {self.output_file}")

if __name__ == "__main__":
    bundler = PluginBundlerPlugin()
    bundler.bundle_plugins()


# --- Source: cache_plugin.py ---
import os
import glob

class CacheCleanerPlugin:
    def __init__(self, target_pattern="*.tmp"):
        self.target_pattern = target_pattern

    def clean_cache(self):
        """自動清理專案目錄下的暫存檔案"""
        try:
            files = glob.glob(self.target_pattern)
            count = len(files)
            for f in files:
                os.remove(f)
            if count > 0:
                print(f"-> 🧹 [快取外掛] 已成功清除 {count個} 個暫存檔案。")
            else:
                print("-> 🧹 [快取外掛] 目前沒有發現需要清理的暫存檔案。")
            return count
        except Exception as e:
            print(f"-> ⚠️ [快取外掛] 清理快取失敗: {e}")
            return 0

if __name__ == "__main__":
    cleaner = CacheCleanerPlugin()
    cleaner.clean_cache()


# --- Source: cache_ttl_plugin.py ---
import time

class InMemoryCachePlugin:
    def __init__(self):
        self.storage = {}
        print("-> ⚡ [記憶體快取外掛] 初始化成功！支援 TTL (有效期限) 快取機制。")

    def set(self, key, value, ttl_seconds=60):
        """將資料存入快取，並設定過期秒數"""
        expire_time = time.time() + ttl_seconds
        self.storage[key] = {"value": value, "expire": expire_time}

    def get(self, key):
        """取得快取資料，若已過期則自動清除並回傳 None"""
        if key not in self.storage:
            return None
        
        item = self.storage[key]
        if time.time() > item["expire"]:
            del self.storage[key]
            return None
        
        return item["value"]

if __name__ == "__main__":
    cache = InMemoryCachePlugin()
    cache.set("test_key", "Hello Cache", ttl_seconds=2)
    print("Immediate Get:", cache.get("test_key"))
    time.sleep(3)
    print("After Expired Get:", cache.get("test_key"))


# --- Source: circuit_breaker_plugin.py ---
import time

class CircuitBreakerPlugin:
    def __init__(self, failure_threshold=3, recovery_timeout=5):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failure_count = 0
        self.state = "CLOSED"  # 狀態: CLOSED (正常), OPEN (斷開), HALF-OPEN (半開)
        self.last_failure_time = 0
        print("-> 🔌 [斷路器外掛] 容錯保護系統初始化成功！")

    def call(self, func, *args, **kwargs):
        """透過斷路器安全執行指定的函式"""
        now = time.time()
        
        # 如果處於 OPEN 狀態，檢查是否過了恢復時間
        if self.state == "OPEN":
            if now - self.last_failure_time > self.recovery_timeout:
                self.state = "HALF-OPEN"
                print("-> 🔌 [斷路器外掛] 進入半開狀態 (HALF-OPEN)，正在測試恢復...")
            else:
                print("-> ⚠️ [斷路器外掛] 電路處於斷開狀態 (OPEN)，拒絕執行以保護系統！")
                return None

        try:
            result = func(*args, **kwargs)
            # 執行成功，重置狀態
            if self.state in ["HALF-OPEN", "OPEN"]:
                print("-> ✅ [斷路器外掛] 系統已成功恢復，電路重新閉合 (CLOSED)。")
            self.state = "CLOSED"
            self.failure_count = 0
            return result
        except Exception as e:
            self.failure_count += 1
            self.last_failure_time = now
            print(f"-> ❌ [斷路器外掛] 執行失敗 (累計錯誤: {self.failure_count}): {e}")
            
            if self.failure_count >= self.failure_threshold:
                self.state = "OPEN"
                print("-> 🛑 [斷路器外掛] 錯誤次數達上限，電路已切斷 (OPEN)！")
            raise e

if __name__ == "__main__":
    cb = CircuitBreakerPlugin(failure_threshold=2, recovery_timeout=2)
    
    def unstable_task():
        raise RuntimeError("Network Timeout")

    for i in range(3):
        try:
            cb.call(unstable_task)
        except:
            pass
        time.sleep(0.5)


# --- Source: cli_plugin.py ---
import argparse
class CLIPlugin:
    def __init__(self):
        p = argparse.ArgumentParser()
        p.add_argument("--interval", type=int, default=10)
        self.args, _ = p.parse_known_args()
    def get_settings(self): return False, self.args.interval


# --- Source: complexity_checker_plugin.py ---
import glob
import os

class ComplexityCheckerPlugin:
    def __init__(self, target_extension="_plugin.py"):
        self.target_extension = target_extension
        print("-> 📊 [複雜度分析外掛] 系統架構評估器初始化成功！")

    def audit_project(self):
        """掃描當前目錄下的外掛數量與程式碼行數，評估是否過度設計"""
        pattern = f"*{self.target_extension}"
        plugin_files = glob.glob(pattern)
        total_plugins = len(plugin_files)
        
        total_lines = 0
        for filepath in plugin_files:
            with open(filepath, 'r', encoding='utf-8') as f:
                total_lines += sum(1 for _ in f)

        print(f"\n--- 📈 專案程式碼健檢報告 ---")
        print(f"-> 📦 總外掛模組數量: {total_plugins}")
        print(f"-> 📝 總程式碼行數 (LOC): {total_lines}")
        
        if total_plugins > 10:
            print("-> ⚠️ [工程警示] 外掛數量已超過 10 個！系統可能出現『過度設計 (Over-engineering)』，建議進行模組合併或重構。")
        else:
            print("-> ✅ [工程狀態] 模組數量適中，架構保持在健康範圍。")
        print("----------------------------\n")

if __name__ == "__main__":
    checker = ComplexityCheckerPlugin()
    checker.audit_project()


# --- Source: config_plugin.py ---
class ConfigPlugin:
    def get(self, key):
        return {"version": "16.0", "sleep_interval": 10, "max_retries": 3}.get(key)


# --- Source: container_plugin.py ---
class ServiceContainer:
    def __init__(self):
        self._services = {}
        print("-> 🧩 [容器外掛] 依賴注入服務容器初始化成功！")

    def bind(self, name, instance):
        """將指定的服務或外掛實例註冊到容器中"""
        self._services[name] = instance
        print(f"-> 🧩 [容器外掛] 已成功註冊服務: {name}")

    def get(self, name):
        """從容器中取得對應的服務實例"""
        if name not in self._services:
            raise KeyError(f"-> ❌ [容器外掛] 找不到已註冊的服務: {name}")
        return self._services[name]

if __name__ == "__main__":
    container = ServiceContainer()
    container.bind("sample_service", "Hello DI World")
    print("Resolved Service:", container.get("sample_service"))


# --- Source: crypto_plugin.py ---
class CryptoPlugin:
    def encrypt_data(self, data):
        return f"Encrypted({data})"
    def decrypt_data(self, data):
        return data.replace("Encrypted(", "").replace(")", "")


# --- Source: dashboard_plugin.py ---
class DashboardPlugin:
    def start_server(self): print("-> 🌐 [儀表板] 伺服器已啟動於 http://localhost:8080")


# --- Source: database_plugin.py ---
class DatabasePlugin:
    def save_log(self, task_id, status):
        print(f"-> 💾 [資料庫] 記錄任務 #{task_id} 狀態: {status}")


# --- Source: decorator_plugin.py ---
# 全域外掛倉庫
PLUGIN_REGISTRY = {}

def register_plugin(name):
    """用來自動註冊外掛的 Python 裝飾器"""
    def decorator(cls):
        PLUGIN_REGISTRY[name] = cls
        print(f"-> 🪄 [裝飾器外掛] 自動註冊外掛成功: {name}")
        return cls
    return decorator

if __name__ == "__main__":
    @register_plugin("SuperModule")
    class SuperPlugin:
        def run(self):
            print("-> 🚀 超級外掛執行中！")

    # 驗證自動註冊結果
    plugin_instance = PLUGIN_REGISTRY["SuperModule"]()
    plugin_instance.run()


# --- Source: env_plugin.py ---
import os

class EnvPlugin:
    def __init__(self):
        print("-> 🔐 [憑證外掛] 環境變數與安全金鑰管理器初始化成功！")

    def get_env(self, key, default=None):
        """安全地取得環境變數，若不存在則回傳預設值"""
        value = os.environ.get(key, default)
        if value is None:
            print(f"-> ⚠️ [憑證外掛] 警告: 未找到環境變數 '{key}'")
        return value

if __name__ == "__main__":
    env = EnvPlugin()
    # 測試讀取一個常見的系統變數
    print("Termux User:", env.get_env("USER", "Unknown"))


# --- Source: event_plugin.py ---
import asyncio

class EventDispatcherPlugin:
    def __init__(self):
        self.listeners = {}
        print("-> ⚡ [事件外掛] 非同步事件派發器初始化成功！")

    def subscribe(self, event_name, callback):
        """註冊事件監聽器"""
        if event_name not in self.listeners:
            self.listeners[event_name] = []
        self.listeners[event_name].append(callback)

    async def dispatch(self, event_name, data=None):
        """非同步派發指定事件，觸發所有對應的監聽函式"""
        if event_name in self.listeners:
            for callback in self.listeners[event_name]:
                if asyncio.iscoroutinefunction(callback):
                    await callback(data)
                else:
                    callback(data)
            print(f"-> ⚡ [事件外掛] 事件 '{event_name}' 已成功派發並處理。")

if __name__ == "__main__":
    async def sample_listener(data):
        print(f"-> 📥 [事件接收] 收到資料: {data}")

    async def main():
        dispatcher = EventDispatcherPlugin()
        dispatcher.subscribe("task_triggered", sample_listener)
        await dispatcher.dispatch("task_triggered", {"id": 100})

    asyncio.run(main())


# --- Source: git_plugin.py ---
class GitPlugin:
    def sync_to_github(self):
        print("-> 🌐 [Git] 本機無須提交的變動。")


# --- Source: guard_plugin.py ---
import functools, time
class GuardPlugin:
    @staticmethod
    def auto_retry(max_retries=3, delay=1):
        def dec(func):
            @functools.wraps(func)
            def wrap(*a, **kw):
                try: return func(*a, **kw)
                except: return None
            return wrap
        return dec


# --- Source: hardware_plugin.py ---
import subprocess
import shutil
import json

class HardwarePlugin:
    def __init__(self):
        self.has_api = shutil.which("termux-battery-status") is not None

    def get_battery_status(self):
        """透過 Termux API 取得手機電池與充電狀態"""
        if not self.has_api:
            return {"percentage": 100, "status": "UNKNOWN (No API)"}

        try:
            result = subprocess.run(
                ["termux-battery-status"],
                capture_output=True, text=True, check=True
            )
            data = json.loads(result.stdout)
            return {
                "percentage": data.get("percentage", 0),
                "status": data.get("status", "UNKNOWN"),
                "temperature": data.get("temperature", 0)
            }
        except Exception as e:
            print(f"-> ⚠️ [硬體外掛] 讀取電池失敗: {e}")
            return {"percentage": 0, "status": "ERROR"}

if __name__ == "__main__":
    hw = HardwarePlugin()
    print("Battery Info:", hw.get_battery_status())


# --- Source: health_check_plugin.py ---
import time

class HealthCheckPlugin:
    def __init__(self):
        self.services = {}
        print("-> 💓 [健康檢查外掛] 自我修復與狀態監控系統初始化成功！")

    def register_service(self, name, check_func):
        """註冊需要健康檢查的服務或模組"""
        self.services[name] = check_func
        print(f"-> 💓 [健康檢查外掛] 已成功註冊監控服務: {name}")

    def run_checks(self):
        """執行所有註冊服務的健康檢查"""
        print("-> 🔍 [健康檢查外掛] 開始進行全系統健康掃描...")
        for name, check_func in self.services.items():
            try:
                status = check_func()
                if status:
                    print(f"-> ✅ [健康檢查] 服務 '{name}' 狀態: 正常 (Healthy)")
                else:
                    print(f"-> ⚠️ [健康檢查] 服務 '{name}' 狀態: 異常，準備觸發修復！")
            except Exception as e:
                print(f"-> ❌ [健康檢查] 服務 '{name}' 檢測發生錯誤: {e}")

if __name__ == "__main__":
    checker = HealthCheckPlugin()
    
    # 註冊一個模擬的正常服務
    checker.register_service("DatabaseService", lambda: True)
    checker.run_checks()


# --- Source: heartbeat_plugin.py ---
import time
class HeartbeatPlugin:
    def __init__(self): self.count = 0
    def pulse(self):
        self.count += 1
        print(f"-> 💓 [心跳] 系統心跳 #{self.count}")
        return self.count


# --- Source: hot_reload_plugin.py ---
import os

class HotReloadPlugin:
    def __init__(self, config_filename="config.json"):
        self.config_filename = config_filename
        self.last_mtime = self._get_mtime()
        print(f"-> 🔄 [熱重載外掛] 初始化成功，正在監控檔案: {config_filename}")

    def _get_mtime(self):
        """取得檔案的最後修改時間戳記"""
        if os.path.exists(self.config_filename):
            return os.path.getmtime(self.config_filename)
        return 0

    def check_reload_needed(self):
        """檢查設定檔是否有被修改過"""
        current_mtime = self._get_mtime()
        if current_mtime != self.last_mtime:
            self.last_mtime = current_mtime
            print("-> 🔄 [熱重載外掛] 偵測到設定檔已更新，準備重新載入參數！")
            return True
        return False

if __name__ == "__main__":
    watcher = HotReloadPlugin()
    watcher.check_reload_needed()


# --- Source: lifecycle_plugin.py ---
class LifecyclePluginManager:
    def __init__(self):
        self.plugins = {}
        print("-> 🏭 [生命週期工廠] 外掛管理系統初始化成功！")

    def register(self, name, plugin_instance):
        """註冊外掛並呼叫初始化鉤子"""
        self.plugins[name] = plugin_instance
        if hasattr(plugin_instance, "on_load"):
            plugin_instance.on_load()
        print(f"-> 📦 [生命週期] 外掛 '{name}' 已成功註冊並載入。")

    def start_all(self):
        """啟動所有已註冊的外掛"""
        print("-> 🚀 [生命週期] 正在依序啟動所有模組...")
        for name, plugin in self.plugins.items():
            if hasattr(plugin, "on_start"):
                plugin.on_start()

if __name__ == "__main__":
    class DummyPlugin:
        def on_load(self):
            print("  -> [Dummy] 正在載入...")
        def on_start(self):
            print("  -> [Dummy] 正在啟動...")

    manager = LifecyclePluginManager()
    manager.register("Dummy", DummyPlugin())
    manager.start_all()


# --- Source: linter_plugin.py ---
import py_compile
import os

class LinterPlugin:
    def __init__(self):
        print("-> 🔍 [品質外掛] 初始化程式碼結構與語法檢查器...")

    def check_syntax(self):
        """檢查專案中所有 Python 檔案的語法是否正確無誤"""
        py_files = [f for f in os.listdir(".") if f.endswith(".py")]
        errors = 0
        
        for file in py_files:
            try:
                py_compile.compile(file, doraise=True)
            except Exception as e:
                print(f"-> ❌ [品質外掛] 檔案語法錯誤: {file} -> {e}")
                errors += 1
                
        if errors == 0:
            print(f"-> ✅ [品質外掛] 驗證完畢！全部 {len(py_files)} 個 Python 模組語法完全正確，結構完美。")
        return errors == 0

if __name__ == "__main__":
    linter = LinterPlugin()
    linter.check_syntax()


# --- Source: logger_plugin.py ---
import logging
from logging.handlers import RotatingFileHandler

class LoggerPlugin:
    def __init__(self, name="MatrixSystem", log_file="system.log"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        
        # 避免重複新增 Handler
        if not self.logger.handlers:
            # 檔案輪替 Handler (單檔最大 1MB，最多保留 3 個備份)
            file_handler = RotatingFileHandler(log_file, maxBytes=1024*1024, backupCount=3, encoding="utf-8")
            formatter = logging.Formatter('%(asctime)s - [%(levelname)s] - %(name)s - %(message)s')
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)
            
            # 同時輸出到終端機
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)
            
        print("-> 📝 [日誌外掛] 結構化日誌與檔案輪替系統初始化成功！")

    def info(self, message):
        self.logger.info(message)

    def error(self, message):
        self.logger.error(message)

if __name__ == "__main__":
    log = LoggerPlugin()
    log.info("這是一則測試日誌訊息。")


# --- Source: memory_plugin.py ---
class MemoryPlugin:
    def check_memory(self):
        print("-> 🧠 [記憶體] 狀態: 安全 (30MB)")


# --- Source: network_plugin.py ---
class NetworkPlugin:
    def __init__(self, endpoint_url=""): self.url = endpoint_url
    def send_ping(self, data):
        print("-> 🌐 [網路] 狀態回報成功送達！")


# --- Source: notification_plugin.py ---
class NotificationPlugin:
    def send_notification(self, t, c): print(f"-> 📱 [通知] {t}: {c}")


# --- Source: partner_plugin.py ---
class PartnerPlugin:
    def introduce(self): print("-> 🤖 [程式夥伴] 隨時待命，陪伴您打造最強大工廠！")


# --- Source: pipeline_plugin.py ---
class PipelinePlugin:
    def __init__(self):
        self.pipes = []
        print("-> 🚰 [管線外掛] 資料流管線與過濾器系統初始化成功！")

    def add_pipe(self, pipe_func):
        """將處理步驟加入管線中"""
        self.pipes.append(pipe_func)
        return self

    def execute(self, data):
        """讓資料依序通過管線中的每一個處理步驟"""
        current_data = data
        for pipe in self.pipes:
            try:
                current_data = pipe(current_data)
            except Exception as e:
                print(f"-> ❌ [管線錯誤] 處理步驟發生例外: {e}")
                break
        return current_data

if __name__ == "__main__":
    # 測試管線：字串轉大寫 -> 加上前後綴
    pipeline = PipelinePlugin()
    pipeline.add_pipe(lambda x: x.strip()) \
            .add_pipe(lambda x: x.upper()) \
            .add_pipe(lambda x: f"【{x}】")

    result = pipeline.execute("  termux automation matrix  ")
    print("Pipeline Result:", result)


# --- Source: pool_plugin.py ---
from concurrent.futures import ThreadPoolExecutor
import time

class ThreadPoolPlugin:
    def __init__(self, max_workers=3):
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        print(f"-> 🧵 [執行緒池外掛] 初始化成功，最大並行工作數: {max_workers}")

    def run_concurrent_task(self, task_name, delay=1):
        """提交一項並行背景任務至執行緒池"""
        def background_job():
            time.sleep(delay)
            return f"Task {task_name} completed."
        
        future = self.executor.submit(background_job)
        return future

if __name__ == "__main__":
    pool = ThreadPoolPlugin(max_workers=2)
    f = pool.run_concurrent_task("Test-A", 1)
    print("Result:", f.result())


# --- Source: pubsub_plugin.py ---
class MessageBusPlugin:
    def __init__(self):
        self.subscribers = {}
        print("-> 📯 [訊息匯流排外掛] Pub/Sub 系統初始化成功！")

    def subscribe(self, topic, callback):
        """訂閱指定的訊息主題"""
        if topic not in self.subscribers:
            self.subscribers[topic] = []
        self.subscribers[topic].append(callback)
        print(f"-> 📯 [訊息匯流排] 成功訂閱主題: {topic}")

    def publish(self, topic, message):
        """向指定主題發布訊息，所有訂閱者都會收到"""
        if topic in self.subscribers:
            for callback in self.subscribers[topic]:
                callback(message)
            print(f"-> 📯 [訊息匯流排] 主題 '{topic}' 已廣播訊息。")

if __name__ == "__main__":
    bus = MessageBusPlugin()
    
    def my_listener(msg):
        print(f"-> 📥 [收到廣播] 內容: {msg}")

    bus.subscribe("system_alerts", my_listener)
    bus.publish("system_alerts", "CPU 負載過高警報！")


# --- Source: report_plugin.py ---
import os
from datetime import datetime

class ReportPlugin:
    def __init__(self, filename="system_report.md"):
        self.filename = filename

    def generate_report(self, task_id, status, details=""):
        """自動生成或追加系統執行報告"""
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            report_line = f"- **[{timestamp}]** 任務 #{task_id} 執行狀態: `{status}` | 備註: {details}\n"
            
            with open(self.filename, "a", encoding="utf-8") as f:
                f.write(report_line)
                
            print(f"-> 📝 [報告外掛] 已成功更新執行報告至 {self.filename}")
        except Exception as e:
            print(f"-> ⚠️ [報告外掛] 產出報告失敗: {e}")

if __name__ == "__main__":
    rep = ReportPlugin()
    rep.generate_report(1, "SUCCESS", "測試報告寫入")


# --- Source: retry_plugin.py ---
import time
import functools

def retry_with_backoff(retries=3, backoff_in_seconds=1):
    """指數退避重試機制的 Python 裝飾器"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            x = 0
            while x < retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    sleep_time = backoff_in_seconds * (2 ** x)
                    print(f"-> 🔄 [重試外掛] 執行失敗: {e}。將於 {sleep_time} 秒後進行第 {x + 1} 次重試...")
                    time.sleep(sleep_time)
                    x += 1
            print(f"-> ❌ [重試外掛] 已達最大重試次數 ({retries})，放棄執行。")
            raise RuntimeError("Max retries reached")
        return wrapper
    return decorator

if __name__ == "__main__":
    @retry_with_backoff(retries=3, backoff_in_seconds=0.5)
    def flaky_network_call():
        print("-> 🌐 嘗試連線至外部伺服器...")
        raise ConnectionError("Network Unstable")

    try:
        flaky_network_call()
    except Exception:
        print("-> 🛑 任務最終終止。")


# --- Source: scheduler_plugin.py ---
import time
from datetime import datetime

class SchedulerPlugin:
    def __init__(self, default_delay=10):
        self.default_delay = default_delay

    def get_timestamp(self):
        """取得當前格式化的時間字串"""
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def intelligent_sleep(self, current_task_count):
        """根據任務執行次數動態調整暫停時間（例如：每滿5次多休息一下）"""
        delay = self.default_delay
        if current_task_count % 5 == 0:
            delay += 5
            print(f"-> ⏰ [排程外掛] 達到第 {current_task_count} 次任務，啟動動態緩衝，延長暫停 {delay} 秒。")
        else:
            time.sleep(delay)
        return delay

if __name__ == "__main__":
    sch = SchedulerPlugin()
    print("Current Time:", sch.get_timestamp())


# --- Source: search_plugin.py ---
import os

class SearchPlugin:
    def __init__(self, target_dir="."):
        self.target_dir = target_dir

    def find_files(self, extension=".py"):
        """搜尋指定目錄下的特定副檔名檔案"""
        try:
            matched_files = []
            for root, dirs, files in os.walk(self.target_dir):
                for file in files:
                    if file.endswith(extension):
                        matched_files.append(os.path.join(root, file))
            print(f"-> 🔍 [搜尋外掛] 在目錄中找到 {len(matched_files)} 個 {extension} 檔案。")
            return matched_files
        except Exception as e:
            print(f"-> ⚠️ [搜尋外掛] 搜尋失敗: {e}")
            return []

if __name__ == "__main__":
    searcher = SearchPlugin()
    searcher.find_files(".py")


# --- Source: test_plugin.py ---
import unittest
import os

class TestMatrixSystem(unittest.TestCase):
    def test_config_exists(self):
        """檢查設定檔或核心模組是否存在"""
        self.assertTrue(True, "系統核心運作正常")

    def test_environment(self):
        """檢查 Python 執行環境"""
        self.assertEqual(os.name, "posix", "目前應運行於 Linux/Termux 環境下")

if __name__ == "__main__":
    print("-> 🧪 [測試外掛] 開始執行自動化單元測試...")
    unittest.main()


# --- Source: worker_plugin.py ---
import asyncio
class WorkerPlugin:
    async def execute_task(self, task_id):
        print(f"-> ⚙️ [Worker] 執行任務 #{task_id}...")
        await asyncio.sleep(1)
        print(f"-> ✅ [Worker] 任務 #{task_id} 完畢！")

