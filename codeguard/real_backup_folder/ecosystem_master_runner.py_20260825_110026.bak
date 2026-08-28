import subprocess
import os

# ==============================================================
# Ecosystem Master Runner - 多語言生態系總控與串聯模組
# ==============================================================

class EcosystemMasterRunner:
    @staticmethod
    def run_all_languages():
        print("=" * 70)
        print(" 🚀 [多語言總控] Genesis-Core-Eternity 跨語言大一統串聯啟動！")
        print("=" * 70)

        # 1. 執行 Python 核心設定與資料庫模組
        print("\n[階段 1/4] 執行 Python 核心模組...")
        if os.path.exists("config_loader.py"):
            subprocess.run(["python", "config_loader.py"])
        else:
            print("-> ⚠️ 找不到 config_loader.py")

        # 2. 執行 JavaScript / Node.js 橋接模組
        print("\n[階段 2/4] 執行 JavaScript / Node.js 模組...")
        if os.path.exists("ecosystem_bridge.js"):
            subprocess.run(["node", "ecosystem_bridge.js"])
        else:
            print("-> ⚠️ 找不到 ecosystem_bridge.js")

        # 3. 編譯並執行 C++ 核心模組
        print("\n[階段 3/4] 編譯並執行 C++ 模組...")
        if os.path.exists("ecosystem_core.cpp"):
            subprocess.run(["g++", "ecosystem_core.cpp", "-o", "ecosystem_core"])
            subprocess.run(["./ecosystem_core"])
        else:
            print("-> ⚠️ 找不到 ecosystem_core.cpp")

        # 4. 編譯並執行 Java 企業級模組
        print("\n[階段 4/4] 編譯並執行 Java 模組...")
        if os.path.exists("EcosystemManager.java"):
            subprocess.run(["javac", "EcosystemManager.java"])
            subprocess.run(["java", "EcosystemManager"])
        else:
            print("-> ⚠️ 找不到 EcosystemManager.java")

        print("\n" + "=" * 70)
        print(" ✨ [串聯完畢] 所有語言生態系核心已成功全部串聯執行完畢！")
        print("=" * 70)

if __name__ == "__main__":
    EcosystemMasterRunner.run_all_languages()

