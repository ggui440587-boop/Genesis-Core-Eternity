import datetime
import os

class StableNoteManager:
    """穩定且不需頻繁修改的筆記管理核心"""
    def __init__(self, filename="stable_notes.txt"):
        self.filename = filename
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        """確保筆記檔案存在，若無則自動建立"""
        if not os.path.exists(self.filename):
            with open(self.filename, "w", encoding="utf-8") as f:
                f.write(f"=== 筆記系統初始化於 {datetime.datetime.now()} ===\n")

    def add_note(self, content):
        """新增筆記到檔案中"""
        if not content.strip():
            print("-> ⚠️ 筆記內容不能為空！")
            return

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            with open(self.filename, "a", encoding="utf-8") as f:
                f.write(f"[{timestamp}] {content}\n")
            print("-> ✅ 筆記已安全存入系統！")
        except Exception as e:
            print(f"-> ❌ 儲存失敗: {e}")

    def read_notes(self):
        """讀取所有歷史筆記"""
        print("\n--- 📚 您的歷史筆記清單 ---")
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                print(f.read())
        except Exception as e:
            print(f"-> ❌ 讀取失敗: {e}")
        print("---------------------------\n")

if __name__ == "__main__":
    manager = StableNoteManager()

    while True:
        print("【穩定筆記系統】")
        print("1. 新增一筆記錄")
        print("2. 查看所有記錄")
        print("3. 離開系統")
        choice = input("請選擇操作 (1/2/3): ").strip()

        if choice == "1":
            text = input("請輸入您的筆記內容: ")
            manager.add_note(text)
        elif choice == "2":
            manager.read_notes()
        elif choice == "3":
            print("-> 系統已安全關閉，祝你有美好的一天！")
            break
        else:
            print("-> ⚠️ 選項錯誤，請重新輸入。\n")

