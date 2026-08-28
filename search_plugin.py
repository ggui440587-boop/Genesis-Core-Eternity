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
