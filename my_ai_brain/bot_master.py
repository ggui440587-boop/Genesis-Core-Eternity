import os
import json
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

print("🧠 [AI 機器人] 本地發片系統啟動中...")

# 檢查憑證是否存在
if not os.path.exists("client_secret.json"):
    print("❌ 找不到 client_secret.json 憑證！")
    exit()

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

# 進行本地授權與取得 Token
flow = InstalledAppFlow.from_client_secrets_file("client_secret.json", scopes=SCOPES)
credentials = flow.run_console()

# 建立 YouTube 服務
youtube = build("youtube", "v3", credentials=credentials)
print("✅ YouTube 授權連線成功！")
