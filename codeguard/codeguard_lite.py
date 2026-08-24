import os
import re
import json
import sys
from pathlib import Path
from datetime import datetime

# ==============================================================
# CodeGuard Lite v6 - 最終商業就緒版
# ==============================================================

DEFAULT_IGNORE_DIRS = {".git", "__pycache__", "venv", "env", "node_modules", "build", "dist"}
DEFAULT_ALLOWED_EXTENSIONS = {".py", ".txt", ".json", ".md", ".sh", ".env"}

SENSITIVE_PATTERNS = [
    r"api[_-]?key\s*=\s*['\"].*?['\"]",
    r"password\s*=\s*['\"].*?['\"]",
    r"secret\s*=\s*['\"].*?['\"]",
    r"token\s*=\s*['\"].*?['\"]"
]

def show_help():
    print("=" * 60)
    print(" CodeGuard Lite 使用說明文件")
    print("=" * 60)
    print(" 用法:")
    print("   python codeguard_lite.py [目標資料夾路徑]")
    print(" 範例:")
    print("   python codeguard_lite.py .          # 掃描當前資料夾")
    print("   python codeguard_lite.py /sdcard/   # 掃描指定路徑")
    print("=" * 60)

def scan_project(target_path):
    abs_target = os.path.abspath(target_path)
    if not os.path.exists(abs_target):
        print(f"[錯誤] 找不到指定的目標資料夾: {abs_target}")
        return

    print(f"[*] 開始執行資安掃描，目標: {abs_target}")
    total_files = 0
    warnings_found = 0
    scan_results = []

    for root, dirs, files in os.walk(abs_target):
        dirs[:] = [d for d in dirs if d not in DEFAULT_IGNORE_DIRS]
        for file in files:
            file_path = Path(root) / file
            if file_path.suffix not in DEFAULT_ALLOWED_EXTENSIONS:
                continue
            total_files += 1
            file_warnings = check_file_security(file_path)
            if file_warnings:
                file_issue_data = {"file": str(file_path), "issues": []}
                for line_no, content in file_warnings:
                    file_issue_data["issues"].append({"line": line_no, "content": content.strip()})
                    warnings_found += 1
                scan_results.append(file_issue_data)

    print(f"[完成] 總檢查檔案: {total_files} | 發現潛在風險: {warnings_found}")
    generate_reports(total_files, warnings_found, scan_results)

def check_file_security(file_path):
    issues = []
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            for line_no, line in enumerate(f, 1):
                for pattern in SENSITIVE_PATTERNS:
                    if re.search(pattern, line, re.IGNORECASE):
                        issues.append((line_no, line))
                        break
    except Exception as e:
        pass
    return issues

def generate_reports(total_files, warnings_found, results):
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    report_data = {
        "tool": "CodeGuard Lite",
        "scan_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "total_files_checked": total_files,
        "total_warnings": warnings_found,
        "details": results
    }
    filename = f"codeguard_report_{timestamp}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(report_data, f, ensure_ascii=False, indent=4)
    print(f"[報表] 已生成檢測報告: {filename}")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] in ["-h", "--help"]:
        show_help()
    else:
        target = sys.argv[1] if len(sys.argv) > 1 else "."
        scan_project(target)

