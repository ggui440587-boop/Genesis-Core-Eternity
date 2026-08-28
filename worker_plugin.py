import asyncio
class WorkerPlugin:
    async def execute_task(self, task_id):
        print(f"-> ⚙️ [Worker] 執行任務 #{task_id}...")
        await asyncio.sleep(1)
        print(f"-> ✅ [Worker] 任務 #{task_id} 完畢！")
