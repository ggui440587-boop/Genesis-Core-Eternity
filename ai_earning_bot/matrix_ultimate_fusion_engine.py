import ast
import asyncio
import importlib.util
import json
import logging
import os
import pathlib
import random
import sqlite3
import subprocess
import sys
import time
import urllib.request

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [ULTIMATE-FUSION] [%(levelname)s] 🌌 %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("ultimate_fusion.log", encoding="utf-8")
    ]
)

class FusionEnvironmentGuard:
    @staticmethod
    def verify():
        if sys.version_info < (3, 7):
            logging.error("【融合中斷】Python 版本必須大於或等於 3.7。")
            sys.exit(1)
        pathlib.Path.cwd().joinpath("plugins").mkdir(exist_ok=True)
        if not os.access(pathlib.Path.cwd(), os.W_OK):
            logging.error("【融合中斷】當前工作目錄無寫入權限。")
            sys.exit(1)
        logging.info("【檢核通過】環境符合全融合引擎的所有真實條件。")

class RealTimePluginLoader:
    def __init__(self, plugin_dir="plugins"):
        self.plugin_dir = pathlib.Path.cwd() / plugin_dir
        self.loaded_plugins = {}

    def load_plugins(self):
        if not self.plugin_dir.exists():
            return []
        active_plugins = []
        for py_file in self.plugin_dir.glob("*.py"):
            plugin_name = py_file.stem
            try:
                if plugin_name not in self.loaded_plugins:
                    spec = importlib.util.spec_from_file_location(plugin_name, str(py_file))
                    if spec and spec.loader:
                        module = importlib.util.module_from_spec(spec)
                        spec.loader.exec_module(module)
                        self.loaded_plugins[plugin_name] = module
                        logging.info(f"【外掛熱載入成功】已載入模組: [{plugin_name}]")
                if plugin_name in self.loaded_plugins:
                    active_plugins.append(self.loaded_plugins[plugin_name])
            except Exception as e:
                logging.error(f"【外掛載入失敗】[{plugin_name}]: {e}")
        return active_plugins

class OmniMorphingDatabaseContext:
    def __init__(self, db_file="matrix_ultimate_fusion.db", state_file="fusion_state.json"):
        self.db_file = db_file
        self.state_file = state_file
        self.state = {"generation": 1, "total_mutations": 0, "git_commit": "unknown"}
        self.load_state()
        self.init_db()

    def load_state(self):
        if os.path.exists(self.state_file):
            try:
                with open(self.state_file, "r", encoding="utf-8") as f:
                    self.state.update(json.load(f))
            except Exception as e:
                logging.error(f"讀取融合狀態失敗: {e}")

    def save_state(self):
        try:
            with open(self.state_file, "w", encoding="utf-8") as f:
                json.dump(self.state, f, ensure_ascii=False, indent=4)
        except Exception as e:
            logging.error(f"保存融合狀態失敗: {e}")

    def init_db(self):
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS fusion_macro_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT,
                    generation INTEGER,
                    mutation_style TEXT,
                    git_commit TEXT,
                    summary TEXT
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS fusion_ast_nodes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT,
                    filename TEXT,
                    node_type TEXT,
                    node_name TEXT,
                    line_no INTEGER
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS omni_flexible_store (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT,
                    generation INTEGER,
                    data_category TEXT,
                    payload_json TEXT
                )
            """)
            conn.commit()
            conn.close()
            logging.info("【資料庫就緒】全融合與萬用吞噬資料表已全數建立。")
        except Exception as e:
            logging.error(f"初始化資料庫失敗: {e}")

    async def log_macro_async(self, mutation_style, commit, summary):
        loop = asyncio.get_running_loop()
        def _write():
            try:
                conn = sqlite3.connect(self.db_file)
                cursor = conn.cursor()
                timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
                cursor.execute(
                    "INSERT INTO fusion_macro_logs (timestamp, generation, mutation_style, git_commit, summary) VALUES (?, ?, ?, ?, ?)",
                    (timestamp, self.state["generation"], mutation_style, commit, summary)
                )
                conn.commit()
                conn.close()
                self.state["generation"] += 1
                self.state["total_mutations"] += 1
            except Exception as e:
                logging.error(f"寫入巨觀日誌失敗: {e}")
        await loop.run_in_executor(None, _write)

    async def log_ast_async(self, filename, n_type, n_name, line):
        loop = asyncio.get_running_loop()
        def _write():
            try:
                conn = sqlite3.connect(self.db_file)
                cursor = conn.cursor()
                timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
                cursor.execute(
                    "INSERT INTO fusion_ast_nodes (timestamp, filename, node_type, node_name, line_no) VALUES (?, ?, ?, ?, ?)",
                    (timestamp, filename, n_type, n_name, line)
                )
                conn.commit()
                conn.close()
            except Exception as e:
                logging.error(f"寫入 AST 節點失敗: {e}")
        await loop.run_in_executor(None, _write)

    async def absorb_omni_data_async(self, category, data):
        loop = asyncio.get_running_loop()
        def _write():
            try:
                conn = sqlite3.connect(self.db_file)
                cursor = conn.cursor()
                timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
                payload_str = json.dumps(data, ensure_ascii=False)
                cursor.execute(
                    "INSERT INTO omni_flexible_store (timestamp, generation, data_category, payload_json) VALUES (?, ?, ?, ?)",
                    (timestamp, self.state["generation"], category, payload_str)
                )
                conn.commit()
                conn.close()
            except Exception as e:
                logging.error(f"全能資料吞噬失敗: {e}")
        await loop.run_in_executor(None, _write)

class UltimateDispatcher:
    def __init__(self, config_file="fusion_config.json"):
        self.config_file = config_file
        self.config_data = {}
        self.load_config()

    def load_config(self):
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, "r", encoding="utf-8") as f:
                    self.config_data = json.load(f)
            except Exception as e:
                logging.error(f"載入設定失敗: {e}")

    def mutate_and_format(self, data_packet):
        self.load_config()
        pool = self.config_data.get("mutation_pool", ["engineering_verbose"])
        selected_style = random.choice(pool)
        languages = self.config_data.get("languages", {})
        template = languages.get(selected_style, "{json_payload}")
        
        format_vars = {
            "generation": data_packet.get("generation"),
            "git_commit": data_packet.get("git_commit"),
            "files_count": data_packet.get("files_count"),
            "timestamp": data_packet.get("timestamp"),
            "mutation_style": selected_style,
            "json_payload": json.dumps(data_packet, ensure_ascii=False)
        }
        try:
            message = template.format(**format_vars)
        except Exception:
            message = json.dumps(data_packet, ensure_ascii=False)
        return message, selected_style

    async def dispatch_async(self, data_packet):
        self.load_config()
        endpoints = self.config_data.get("production_endpoints", [])
        if not endpoints:
            return
        message_content, style_used = self.mutate_and_format(data_packet)
        payload = json.dumps({"mutation_style": style_used, "content": message_content, "raw_data": data_packet}).encode("utf-8")
        
        for ep in endpoints:
            if not ep.get("enabled", True):
                continue
            url = ep.get("url")
            name = ep.get("name", "unknown")
            req = urllib.request.Request(
                url, data=payload,
                headers={"Content-Type": "application/json", "User-Agent": "UltimateFusion/1.0"},
                method="POST"
            )
            try:
                loop = asyncio.get_running_loop()
                response = await loop.run_in_executor(None, lambda: urllib.request.urlopen(req, timeout=6.0))
                with response:
                    if response.status in [200, 201]:
                        logging.info(f"【平行推送成功】端點 [{name}] | 突變風格: [{style_used}]")
            except Exception as e:
                logging.error(f"【平行推送失敗】[{name}]: {e}")

class UltimateFusionEngine:
    def __init__(self):
        FusionEnvironmentGuard.verify()
        self.db_context = OmniMorphingDatabaseContext()
        self.dispatcher = UltimateDispatcher()
        self.plugin_loader = RealTimePluginLoader()
        self.loop_interval = 10.0
        logging.info("初始化終極全融合矩陣引擎...")

    def get_git_commit(self):
        try:
            res = subprocess.run(["git", "rev-parse", "--short", "HEAD"], capture_output=True, text=True, timeout=3)
            if res.returncode == 0:
                commit = res.stdout.strip()
                self.db_context.state["git_commit"] = commit
                return commit
        except Exception:
            pass
        return "non_git_workspace"

    async def scan_ast_async(self):
        cwd = pathlib.Path.cwd()
        py_files = [f for f in cwd.glob("*.py") if f.name != "matrix_ultimate_fusion_engine.py"]
        for py_file in py_files:
            try:
                loop = asyncio.get_running_loop()
                content = await loop.run_in_executor(None, lambda: py_file.read_text(encoding="utf-8"))
                tree = ast.parse(content, filename=str(py_file))
                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef):
                        await self.db_context.log_ast_async(py_file.name, "FUNCTION", node.name, node.lineno)
                    elif isinstance(node, ast.ClassDef):
                        await self.db_context.log_ast_async(py_file.name, "CLASS", node.name, node.lineno)
            except Exception as e:
                logging.error(f"解析 AST 失敗 [{py_file.name}]: {e}")

    async def execute_cycle(self):
        commit = self.get_git_commit()
        file_count = len([f for f in pathlib.Path.cwd().iterdir() if f.is_file()])
        summary = f"Ultimate Fusion Cycle. Files: {file_count}, Commit: {commit}"
        
        logging.info(f"【全融合心跳】世代 [{self.db_context.state['generation']}] 開始運作...")
        await self.scan_ast_async()
        
        plugins = self.plugin_loader.load_plugins()
        for plugin in plugins:
            if hasattr(plugin, "run_fusion_task"):
                try:
                    if asyncio.iscoroutinefunction(plugin.run_fusion_task):
                        plugin_data = await plugin.run_fusion_task()
                    else:
                        plugin_data = plugin.run_fusion_task()
                    if plugin_data:
                        await self.db_context.absorb_omni_data_async("plugin_payload", plugin_data)
                except Exception as e:
                    logging.error(f"外掛執行例外: {e}")

        packet = {
            "source": "Ultimate-Fusion-Nexus",
            "generation": self.db_context.state["generation"],
            "git_commit": commit,
            "files_count": file_count,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        message, style_used = self.dispatcher.mutate_and_format(packet)
        await self.dispatcher.dispatch_async(packet)
        await self.db_context.log_macro_async(style_used, commit, summary)
        self.db_context.save_state()

    async def start_daemon(self):
        logging.info("【引擎點火】終極全融合背景守護行程正式啟動...")
        try:
            while True:
                try:
                    await self.execute_cycle()
                except Exception as e:
                    logging.warning(f"【例外攔截】{e}")
                await asyncio.sleep(self.loop_interval)
        except asyncio.CancelledError:
            logging.info("【引擎終止】任務被安全取消。")
        except KeyboardInterrupt:
            logging.info("【引擎休眠】手動中斷，全融合狀態已安全封存。")
            self.db_context.save_state()

if __name__ == "__main__":
    engine = UltimateFusionEngine()
    try:
        asyncio.run(engine.start_daemon())
    except KeyboardInterrupt:
        print("終極全融合引擎已安全退出。")
