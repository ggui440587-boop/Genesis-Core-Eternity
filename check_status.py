import os

def check_system():
    print("-> 🔍 [系統檢查] 正在掃描當前專案的外掛完整性...")
    plugins = [
        "worker_plugin.py", "database_plugin.py", "git_plugin.py",
        "heartbeat_plugin.py", "memory_plugin.py", "crypto_plugin.py",
        "network_plugin.py", "backup_plugin.py", "benchmark_plugin.py",
        "cli_plugin.py", "guard_plugin.py", "config_plugin.py",
        "dashboard_plugin.py", "notification_plugin.py", "partner_plugin.py",
        "main_controller.py"
    ]
    
    missing = [p for p in plugins if not os.path.exists(p)]
    if not missing:
        print("-> ✅ [系統檢查] 太棒了！所有十六大外掛與主控制器全數就位，結構完美！")
    else:
        print(f"-> ⚠️ [系統檢查] 缺少的檔案: {missing}")

if __name__ == "__main__":
    check_system()
