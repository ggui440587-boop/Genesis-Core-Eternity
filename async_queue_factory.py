import asyncio
import datetime
import random

async def producer(queue, name):
    for i in range(3):
        await asyncio.sleep(1)
        task_data = f"Gene-Asset-{name}-{i}"
        await queue.put(task_data)
        print(f"-> 🧬 [生產者 {name}] 已產出並放入佇列: {task_data}")

async def consumer(queue, worker_id):
    while True:
        task = await queue.get()
        print(f"-> ⚙️ [消費者 #{worker_id}] 正在處理任務: {task}")
        await asyncio.sleep(1.5)  # 模擬非同步運算、編譯或寫入
        print(f"-> ✅ [消費者 #{worker_id}] 任務完成: {task}")
        queue.task_done()

async def main():
    queue = asyncio.Queue()

    print("【非同步訊息佇列生產線啟動】")
    
    # 啟動生產者與消費者任務
    producer_tasks = [
        asyncio.create_task(producer(queue, "Grok")),
        asyncio.create_task(producer(queue, "Kimi"))
    ]
    
    consumer_tasks = [
        asyncio.create_task(consumer(queue, 1)),
        asyncio.create_task(consumer(queue, 2))
    ]

    # 等待所有生產者完成
    await asyncio.gather(*producer_tasks)
    
    # 等待佇列中的任務全部被消費完畢
    await queue.join()
    
    # 取消消費者背景任務
    for c in consumer_tasks:
        c.cancel()
        
    print("-> 🎉 所有非同步佇列任務圓滿處理完畢！")

if __name__ == "__main__":
    asyncio.run(main())
