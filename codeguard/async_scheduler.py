import asyncio
import datetime

# ==============================================================
# Async Scheduler Module - 非同步並行任務排程與調度模組
# ==============================================================

class AsyncScheduler:
    @staticmethod
    async def background_study_task():
        """非同步背景讀書任務"""
        print("📖 [非同步讀書] 開始背景吸收知識...")
        await asyncio.sleep(1)  # 模擬非同步 I/O 等待
        print("📖 [非同步讀書] 知識吸收完畢！")

    @staticmethod
    async def background_action_task():
        """非同步背景動起來任務"""
        print("⚡ [非同步行動] 開始動態運算與執行任務...")
        await asyncio.sleep(1.5)
        print("⚡ [非同步行動] 任務執行完畢！")

    @classmethod
    async def run_ecosystem_pipeline(cls):
        """同時調度多個模組並行運行，提升執行效率"""
        print("=" * 60)
        print(f" 🚀 [非同步核心] 啟動全生態系並行調度管線...")
        print("=" * 60)

        start_time = datetime.datetime.now()

        # 使用 asyncio.gather 同時執行多個獨立模組
        await asyncio.gather(
            cls.background_study_task(),
            cls.background_action_task()
        )

        end_time = datetime.datetime.now()
        print("=" * 60)
        print(f" ✨ [執行完畢] 所有非同步任務已完成，總耗時: {end_time - start_time}")
        print("=" * 60)

if __name__ == "__main__":
    # 在主迴圈中運行非同步排程
    asyncio.run(AsyncScheduler.run_ecosystem_pipeline())

