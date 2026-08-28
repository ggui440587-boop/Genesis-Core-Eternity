class PipelinePlugin:
    def __init__(self):
        self.pipes = []
        print("-> 🚰 [管線外掛] 資料流管線與過濾器系統初始化成功！")

    def add_pipe(self, pipe_func):
        """將處理步驟加入管線中"""
        self.pipes.append(pipe_func)
        return self

    def execute(self, data):
        """讓資料依序通過管線中的每一個處理步驟"""
        current_data = data
        for pipe in self.pipes:
            try:
                current_data = pipe(current_data)
            except Exception as e:
                print(f"-> ❌ [管線錯誤] 處理步驟發生例外: {e}")
                break
        return current_data

if __name__ == "__main__":
    # 測試管線：字串轉大寫 -> 加上前後綴
    pipeline = PipelinePlugin()
    pipeline.add_pipe(lambda x: x.strip()) \
            .add_pipe(lambda x: x.upper()) \
            .add_pipe(lambda x: f"【{x}】")

    result = pipeline.execute("  termux automation matrix  ")
    print("Pipeline Result:", result)
