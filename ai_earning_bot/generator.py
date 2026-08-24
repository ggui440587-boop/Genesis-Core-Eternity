import os
import google.generativeai as genai
from datetime import datetime

# 設定你的 Gemini API Key
GOOGLE_API_KEY = "AQ.Ab8RN6JOliVUP_vhxjatYWIraxRUtDqEy4mnWeS-CjEfii4ynA"
genai.configure(api_key=GOOGLE_API_KEY)

def generate_article():
    # 這裡可以替換成你想讓 AI 幫你寫的主題
    prompt = """
    請以專業且好讀的繁體中文，寫一篇關於「近期 AI 工具與開源技術發展趨勢」的短篇懶人包文章。
    內容需包含：
    1. 吸引人的標題
    2. 3個近期值得關注的重點技術或工具介紹
    3. 結語與對開發者/一般人的實用建議
    文章風格要流暢、自然，適合發布在部落格上。
    """
    
    print("正在呼叫 AI 生成內容...")
    model = genai.GenerativeModel('gemini-2.5-flash')
    response = model.generate_content(prompt)
    
    # 加上日期作為檔名
    today = datetime.now().strftime("%Y-%m-%d_%H%M")
    filename = f"output/post_{today}.md"
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(response.text)
        
    print(f"文章已成功生成並儲存至：{filename}")

if __name__ == "__main__":
    generate_article()

