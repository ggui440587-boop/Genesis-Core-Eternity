import functools
import traceback

class ExceptionHandlerModule:
    @staticmethod
    def safe_execute(task_name="Genesis_Task"):
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                try:
                    print(f"-> 🛡️ [SafeExecute] 開始安全執行: {task_name}")
                    result = func(*args, **kwargs)
                    print(f"   [✓] {task_name} 執行成功。")
                    return result
                except Exception as e:
                    print(f"   [✕] 警告：{task_name} 執行過程中發生異常！")
                    print(f"   [錯誤詳情]: {e}")
                    return None
            return wrapper
        return decorator

if __name__ == "__main__":
    # 測試安全執行裝飾器
    @ExceptionHandlerModule.safe_execute(task_name="Test_Task")
    def faulty_task():
        raise ValueError("模擬的測試錯誤")

    faulty_task()

