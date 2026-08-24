import json
import os
import random
import time
import urllib.request

# 1. 已經直接將 API Key 融進程式碼中（免手動 export）
API_KEY = "AQ.Ab8RN6JOliVUP_vhxjatYWIraxRUtDqEy4mnWeS-CjEfii4ynA"

# 2. 你的 JOYTEL 專屬推廣連結（已套用 FB/IG 適用格式）
JOYTEL_LINK = "https://affclkr.com/track/clicks/8561/c627c2bc9b0420d8f98fec23d62e9e452c6c4bce63b2a0f90f65b40471401de3c021e7e5593c99616c"

# 3. 行業與專屬連結對應表
INDUSTRY_AFFILIATE_MAP = {
    "自由工作者": {
        "category_name": "JOYTEL 出國網卡與行動通訊",
        "link": JOYTEL_LINK,
    },
    "斜槓副業經營者": {
        "category_name": "JOYTEL 數位遊牧網路方案",
        "link": JOYTEL_LINK,
    },
    "軟體工程師": {
        "category_name": "JOYTEL 遠距辦公高速上網",
        "link": JOYTEL_LINK,
    },
    "行銷企劃": {
        "category_name": "JOYTEL 出差行動上網方案",
        "link": JOYTEL_LINK,
    },
    "餐飲創業家": {
        "category_name": "JOYTEL 行動通訊與網路支援",
        "link": JOYTEL_LINK,
    },
}

# 4. 發布平台風格設定
PLATFORM_RULES = {
    "vocus": {
        "name": "方格子 (vocus)",
        "style": (
            "像是一位成熟的職場前輩或創作者在寫專欄。語氣要真誠、有故事感、帶有深刻的"
            "個人反思，絕對不要有罐頭腔。"
        ),
    },
    "instagram": {
        "name": "Instagram",
        "style": (
            "像是在跟朋友傳訊息吐露心聲。開頭第一句戳中痛點，短句居多、留白多，"
            "結尾帶有強烈共鳴與熱門 Hashtags。"
        ),
    },
}


def call_gemini_api(prompt_text):
  url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={API_KEY}"
  headers = {"Content-Type": "application/json"}
  data = {"contents": [{"parts": [{"text": prompt_text}]}]}

  req = urllib.request.Request(
      url,
      data=json.dumps(data).encode("utf-8"),
      headers=headers,
      method="POST",
  )
  try:
    with urllib.request.urlopen(req) as response:
      res_json = json.loads(response.read().decode("utf-8"))
      return res_json["candidates"][0]["content"]["parts"][0]["text"]
  except Exception as e:
    return f"API 呼叫失敗: {str(e)}"


def run_task():
  industry = random.choice(list(INDUSTRY_AFFILIATE_MAP.keys()))
  selected_affiliate = INDUSTRY_AFFILIATE_MAP[industry]

  platform_key = random.choice(list(PLATFORM_RULES.keys()))
  rule = PLATFORM_RULES[platform_key]

  print(
      f"\n[AI-CORE] 正在用 Gemini 打造【{industry}】的【{rule['name']}】專屬文案..."
  )

  prompt = f"""
    你是一位極具個人魅力的資深內容創作者，正在寫一篇要在網路上引起共鳴的熱門貼文。
    
    【目標讀者/行業】：{industry}
    【發布平台】：{rule['name']}
    【寫作風格與靈魂】：
    {rule['style']}
    - 嚴禁使用「總而言之」、「首先」、「不可否認」等機械式AI轉折詞。
    
    【核心主題與配圖說明】：
    - 現代人在該行業中面臨的「效率焦慮、數位內耗或出國出差、遠距工作需求」的真實心境。
    - 本篇貼文建議搭配 **JOYTEL 官方提供的精美網卡/eSIM產品素材圖片** 來發布。
    
    請依照以下格式完整輸出：
    ---
    【官方素材搭配建議】
    (說明這篇文案最適合搭配哪一種官方素材圖片)
    ---
    【正文內容】
    (擬人化文案內容)
    """

  content_result = call_gemini_api(prompt)

  # 合規宣告與聯盟網條款提醒
  footer_section = f"""
---
💡 **數位遊牧與行動通訊推薦**：
👉 探索穩定順暢的 {selected_affiliate['category_name']}：{selected_affiliate['link']}

📌 **誠實宣告與下單貼心提醒**：
- 本篇內容包含聯盟行銷推廣連結。透過此連結購買不會增加您的花費，但我會獲得微薄分潤以支持內容創作（有效訂單將於 7 天鑑賞期無退貨後生效）。
- **結帳小提醒**：若選擇 ATM、超商代碼或信用卡付款，完成付款後**請務必點擊「返回商店」**，才能確保系統順利追蹤到您的專屬福利喔！所有分享僅供參考。
"""

  final_output = content_result + footer_section

  # 自動歸檔儲存
  dir_path = os.path.join("posts", platform_key, industry)
  os.makedirs(dir_path, exist_ok=True)
  filename = os.path.join(dir_path, f"post_{int(time.time())}.txt")

  with open(filename, "w", encoding="utf-8") as f:
    f.write(final_output)

  print(f"[SUCCESS] 檔案已自動分類並安全儲存至: {filename}")


if __name__ == "__main__":
  print("[SERVER] 自動化內容與合規聯盟行銷管線已啟動...")
  run_task()
	

