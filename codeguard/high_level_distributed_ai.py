import asyncio
import datetime
import logging

# 設定高等級系統日誌
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] 🌐 [分散式中樞]: %(message)s"
)

class HighLevelDistributedAIHub:
    def __init__(self):
        logging.info("初始化高等級分散式 AI 事件驅動中樞...")
        self.task_queue = asyncio.Queue()

    async def event_producer(self):
        """模擬系統持續接收並派送非同步任務"""
        tasks = [
            {"task_id": "T-101", "payload": "解析本地知識庫 RAG 檔案"},
            {"task_id": "T-102", "payload": "執行自動化代理人任務迴圈"},
            {"task_id": "T-103", "payload": "產出企業級運算與安全日誌"}
        ]

        for t in tasks:
            await asyncio.sleep(0.5) # 模擬網路或事件延遲
            logging.info(f"發布新任務至佇列 -> ID: {t['task_id']}")
            await self.task_queue.put(t)

        # 放入結束信號
        await self.task_queue.put(None)

    async def ai_worker_consumer(self, worker_name):
        """非同步 AI 工作節點：持續從佇列中獲取任務並進行平行處理"""
        logging.info(f"AI 工作節點 [{worker_name}] 已上線並開始監聽佇列。")

        while True:
            task = await self.task_queue.get()
            if task is None:
                # 將結束信號放回，讓其他 worker 也能正常退出
                await self.task_queue.put(None)
                break

            timestamp = datetime.datetime.now().strftime("%H:%M:%S")
            logging.info(f"[{worker_name}] 正在執行任務 [{task['task_id']}]: {task['payload']}")

            # 模擬 AI 非同步運算與推理延遲
            await asyncio.sleep(1.0)

            logging.info(f"[{worker_name}] 任務 [{task['task_id']}] 執行完畢！")
            self.task_queue.task_done()

    async def run_cluster(self):
        """啟動分散式叢集主循環"""
        logging.info("啟動分散式 AI 叢集生命週期...")

        # 建立一個生產者與兩個非同步 AI 工作節點
        producer = asyncio.create_task(self.event_producer())
        worker_1 = asyncio.create_task(self.ai_worker_consumer("AI-Node-Alpha"))
        worker_2 = asyncio.create_task(self.ai_worker_consumer("AI-Node-Beta"))

        # 等待所有非同步任務執行完成
        await asyncio.gather(producer, worker_1, worker_2)
        logging.info("所有分散式任務已完美處理完畢，叢集安全關閉。")

if __name__ == "__main__":
    hub = HighLevelDistributedAIHub()
    asyncio.run(hub.run_cluster())

