import logging
from logging.handlers import RotatingFileHandler

class LoggerPlugin:
    def __init__(self, name="MatrixSystem", log_file="system.log"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        
        # 避免重複新增 Handler
        if not self.logger.handlers:
            # 檔案輪替 Handler (單檔最大 1MB，最多保留 3 個備份)
            file_handler = RotatingFileHandler(log_file, maxBytes=1024*1024, backupCount=3, encoding="utf-8")
            formatter = logging.Formatter('%(asctime)s - [%(levelname)s] - %(name)s - %(message)s')
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)
            
            # 同時輸出到終端機
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)
            
        print("-> 📝 [日誌外掛] 結構化日誌與檔案輪替系統初始化成功！")

    def info(self, message):
        self.logger.info(message)

    def error(self, message):
        self.logger.error(message)

if __name__ == "__main__":
    log = LoggerPlugin()
    log.info("這是一則測試日誌訊息。")
