import re

with open("cloud_pipeline_hub.py", "r", encoding="utf-8") as f:
    content = f.read()

# 自動替換成你的專屬 Webhook 網址
new_url = "https://hook.us2.make.com/ido4wy3xyjfipl9164nm891a1dstn0a3"
content = re.sub(r'CLOUD_WEBHOOK_URL = ".*?"', f'CLOUD_WEBHOOK_URL = "{new_url}"', content)

with open("cloud_pipeline_hub.py", "w", encoding="utf-8") as f:
    f.write(content)

print("[SUCCESS] 雲端 Webhook 網址已成功寫入 cloud_pipeline_hub.py！")
