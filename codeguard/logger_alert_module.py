import logging
import datetime

class SystemLogger:
    def __init__(self, log_file="genesis_system.log"):
        self.log_file = log_file
        logging.basicConfig(
            filename=self.log_file,
            level=logging.INFO,
            format="%(asctime)s [%(levelname)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

    def log_info(self, message):
        logging.info(message)
        print(f"-> [INFO] {message}")

    def log_error(self, message):
        logging.error(message)
        print(f"-> [ERROR] ⚠️ {message}")

if __name__ == "__main__":
    logger = SystemLogger()
    logger.log_info("系統日誌模組初始化測試成功。")

