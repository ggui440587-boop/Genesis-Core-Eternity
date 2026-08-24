import os
import shutil
from pathlib import Path

# 定義副檔名與分類資料夾的對照關係
CATEGORIES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp", ".svg"],
    "Videos": [".mp4", ".mkv", ".avi", ".mov", ".flv", ".webm"],
    "Audio": [".mp3", ".wav", ".flac", ".aac", ".m4a", ".ogg"],
    "Documents": [".pdf", ".docx", ".doc", ".txt", ".xlsx", ".pptx", ".csv", ".epub"],
    "Code": [".py", ".sh", ".html", ".css", ".js", ".json", ".xml", ".sql"],
    "Archives": [".zip", ".tar", ".gz", ".7z", ".rar"],
    "Executables": [".apk", ".deb"]
}

def get_category(file_extension):
    """依據副檔名回傳對應的分類資料夾名稱"""
    ext = file_extension.lower()
    for category, extensions in CATEGORIES.items():
        if ext in extensions:
            return category
    return "Others"  # 未定副檔名歸類至 Others

def organize_folder(target_dir):
    """執行指定資料夾內的檔案自動分類"""
    target_path = Path(target_dir)

    if not target_path.exists():
        print(f"[❌ 錯誤] 找不到指定的路徑：{target_dir}")
        return

    print(f"=== 開始整理目標資料夾：{target_path.absolute()} ===\n")
    moved_count = 0

    for item in target_path.iterdir():
        # 只處理檔案，跳過子資料夾
        if item.is_file() and not item.name.startswith("."):
            category = get_category(item.suffix)
            dest_dir = target_path / category
            
            # 自動建立分類資料夾
            dest_dir.mkdir(exist_ok=True)
            
            dest_file = dest_dir / item.name

            # 防止檔名衝突，若存在同名檔案自動重命名
            if dest_file.exists():
                stem = item.stem
                suffix = item.suffix
                dest_file = dest_dir / f"{stem}_copy{suffix}"

            try:
                shutil.move(str(item), str(dest_file))
                print(f"[✅ 搬移] {item.name} -> {category}/")
                moved_count += 1
            except Exception as e:
                print(f"[⚠️ 失敗] 無法搬移 {item.name}：{e}")

    print(f"\n=== 整理完成！共成功整理了 {moved_count} 個檔案 ===")

if __name__ == "__main__":
    # 預設整理目前目錄，也可以改為 Termux 下載區路徑："/sdcard/Download"
    TARGET_PATH = "./"
    organize_folder(TARGET_PATH)

