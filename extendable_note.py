import datetime
import os

# 1. 基礎類別：負責最核心的儲存與讀取（寫好後就不需要再修改它）
class BaseNoteManager:
    def __init__(self, filename="my_permanent_records.txt"):
        self.filename = filename

    def add_record(self, text):
        if not text.strip():
            print("-> ⚠️ 內容不能為空！")
            return
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.filename, "a", encoding="utf-8") as f:
            f.write(f"[{now}] {text}\n")
        print("-> ✅ 記錄成功！")

    def view_records(self):
        print("\n--- 📂 所有歷史記錄 ---")
        if not os.path.exists(self.filename):
            print("目前還沒有任何記錄。")
            return
        with open(self.filename, "r", encoding="utf-8") as f:
            print(f.read())
        print("-----------------------")

# 2. 擴充類別：透過繼承 BaseNoteManager，直接擁有舊功能，並安全地加入「搜尋」新功能
class AdvancedNoteManager(BaseNoteManager):
    def search_records(self, keyword):
        print(f"\n--- 🔍 搜尋關鍵字: 「{keyword}」 ---")
        if not os.path.exists(self.filename):
            print("找不到記錄檔案。")
            return

        found = False
        with open(self.filename, "r", encoding="utf-8") as f:
            for line in f:
                if keyword in line:
                    print(line.strip())
                    found = True
        if not found:
            print("沒有找到符合的記錄。")
        print("-----------------------")

if __name__ == "__main__":
    # 使用擴充後的管理器，既有原本的功能，又能使用新功能
    manager = AdvancedNoteManager()

    while True:
        print("\n【可擴充的筆記系統】")
        print("1. 新增記錄")
        print("2. 查看記錄")
        print("3. 搜尋記錄 (新擴充功能)")
        print("4. 離開")
        choice = input("請選擇功能 (1/2/3/4): ").strip()

        if choice == "1":
            text = input("請輸入要記錄的內容: ")
            manager.add_record(text)
        elif choice == "2":
            manager.view_records()
        elif choice == "3":
            kw = input("請輸入要搜尋的關鍵字: ")
            manager.search_records(kw)
        elif choice == "4":
            print("-> 程式已安全關閉。")
            break
        else:
            print("-> ⚠️ 輸入錯誤，請重新選擇。")

