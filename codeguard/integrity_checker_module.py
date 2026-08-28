import hashlib
import os

class IntegrityCheckerModule:
    def __init__(self, target_files=None):
        self.target_files = target_files or ["core_engine.py", "optimizer.c"]

    def compute_hashes(self):
        print("-> 🔒 [IntegrityChecker] 開始計算專案檔案雜湊校驗值...")
        results = {}

        for filepath in self.target_files:
            if os.path.exists(filepath):
                hasher = hashlib.sha256()
                with open(filepath, "rb") as f:
                    buf = f.read()
                    hasher.update(buf)
                file_hash = hasher.hexdigest()
                results[filepath] = file_hash
                print(f"   [✓] 檔案 {filepath} 雜湊值: {file_hash[:16]}...")
            else:
                print(f"   [!] 找不到目標檔案: {filepath}")

        return results

if __name__ == "__main__":
    checker = IntegrityCheckerModule()
    checker.compute_hashes()

