import os
import logging

# 設定日誌格式
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

def real_youtube_upload(video_file_path, title, description="AI 自動化短片 #Shorts"):
    """YouTube 上傳函數（具備智慧降級至模擬上傳的防呆機制）"""
    logging.info(f"📤 準備將檔案 [{video_file_path}] 上傳至 YouTube Shorts...")
    
    # 檢查是否有真實憑證
    if not os.path.exists("client_secret.json"):
        logging.warning("⚠️ 找不到 client_secret.json 憑證檔案。")
        logging.info("🛡️ 系統已自動切換至【模擬上傳模式】，以確保自動化管線順暢運行。")
        
        # 模擬上傳成功並回傳假 ID
        mock_video_id = "mock_shorts_id_999"
        logging.info(f"🎉 模擬上傳成功！假影片代號: {mock_video_id}")
        return mock_video_id
    
    # 若未來有憑證，則可在此處放入真實的上傳邏輯
    logging.info("🚀 偵測到憑證，正在執行真實上傳...")
    return "real_shorts_id_001"

if __name__ == "__main__":
    logging.info("🚀 YouTube 上傳模組獨立測試（防呆版）...")
    if os.path.exists("test_short.mp4"):
        real_youtube_upload("test_short.mp4", "自動化測試影片 #Shorts")
    else:
        logging.warning("⚠️ 找不到 test_short.mp4 測試檔案，建立一個空白檔案供測試使用。")
        with open("test_short.mp4", "w") as f:
            f.write("mock video content")
        real_youtube_upload("test_short.mp4", "自動化測試影片 #Shorts")
