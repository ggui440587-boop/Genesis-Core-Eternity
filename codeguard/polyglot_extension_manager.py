import os

# ==============================================================
# Polyglot Extension Manager - 多語言擴充套件管理模組
# ==============================================================

class PolyglotExtensionManager:
    SUPPORTED_LANGUAGES = {
        "Python": "extension_python.py",
        "JavaScript": "extension_bridge.js",
        "C/C++": "extension_core.cpp",
        "Java": "ExtensionManager.java",
        "Rust": "extension_safe.rs",
        "C#": "ExtensionRunner.cs"
    }

    @classmethod
    def scan_and_report_extensions(cls):
        print("=" * 65)
        print(" 🧩 [多語言擴充] 正在掃描各程式語言專屬擴充模組...")
        print("=" * 65)

        for lang, filename in cls.SUPPORTED_LANGUAGES.items():
            if os.path.exists(filename):
                print(f"-> 🟢 [{lang}] 擴充模組已就緒: {filename}")
            else:
                print(f"-> 🟡 [{lang}] 尚未建立擴充檔案 ({filename})，可隨時編寫掛載。")

        print("=" * 65)

if __name__ == "__main__":
    PolyglotExtensionManager.scan_and_report_extensions()

