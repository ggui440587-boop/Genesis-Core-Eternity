import os
import time
import logging
import requests

# 統一整合所有真實 API 金鑰與憑證
API_KEYS = {
    "Groq": "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",
    "DeepSeek": "sk-049494902edc4520b4dc347aa9a512b2",
    "OpenAI": "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",
    "Kling": "api-key-kling-H1C8UYZ1_yShxFVTv9K2t83XjGT6oWIp3lDbtMIBncI",
    "Luma": "luma-api-0SdY2t3swF2Dq5liinfAHNwarvmBG1VTXXYHB4dTXPg"
}

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

def real_generate_text(prompt):
    """真實調用 Groq API 進行文字或腳本生成"""
    headers = {
        "Authorization": f"Bearer {API_KEYS['Groq']}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "llama3-70b-8192",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }
    try:
        response = requests.post("https://api.groq.com/openai/v1/chat/completions", json=payload, headers=headers, timeout=15)
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            logging.error(f"Groq API 錯誤狀態碼 {response.status_code}: {response.text}")
    except Exception as e:
        logging.error(f"Groq API 請求發生例外狀況: {e}")
    return None

if __name__ == "__main__":
    logging.info("🧬 全真實 API 整合引擎已啟動...")
    sample_text = real_generate_text("請為 YouTube Shorts 寫一段關於 AI 自動化的吸引人開場白")
    if sample_text:
        logging.info(f"AI 真實生成結果:\n{sample_text}")
    else:
        logging.error("未能成功取得 AI 生成結果，請檢查上方錯誤日誌。")
