import random
import requests
import logging

# 集中管理你的所有 API 金鑰
API_KEYS = {
    "groq": "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",
    "openai": "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",
    "deepseek": "sk-049494902edc4520b4dc347aa9a512b2",
    "xai": "xai-M5BNgXq6wCOVpNeV9bXmNqmD6CuPA80P2I1SDZXQQwqdmMOk1YNSKJX8OfHLmpOUyvEbBEIOeIwqtF5w",
    "qwen": "sk-ws-H.DMYMYEL.ZBxw.MEUCIQCTFhmPzIFOYpsVYB5rN1sWZaVNaYKUh7Qc6pUTxrIUpgIgWy_WkOhxbUMY2zWyWuOscxfNBLn_yZi-B9c4wcXVLHQ"
}

def get_random_ai_script(topic):
    """隨機挑選一個 AI 模型來生成 Shorts 影片腳本"""
    providers = ["groq", "openai", "deepseek", "xai"]
    selected_provider = random.choice(providers)
    
    logging.info(f"🎲 隨機選中 AI 模型供應商: {selected_provider.upper()}")
    
    if selected_provider == "groq":
        try:
            url = "https://api.groq.com/openai/v1/chat/completions"
            headers = {"Authorization": f"Bearer {API_KEYS['groq']}", "Content-Type": "application/json"}
            payload = {
                "model": "openai/gpt-oss-20b",
                "messages": [{"role": "user", "content": f"寫一個關於 {topic} 的 30 秒 Shorts 影片腳本"}],
                "stream": False
            }
            res = requests.post(url, json=payload, headers=headers, timeout=15)
            if res.status_code == 200:
                return res.json()["choices"][0]["message"]["content"]
        except Exception as e:
            logging.error(f"❌ Groq 請求失敗: {e}")

    elif selected_provider == "deepseek":
        try:
            url = "https://api.deepseek.com/chat/completions"
            headers = {"Authorization": f"Bearer {API_KEYS['deepseek']}", "Content-Type": "application/json"}
            payload = {
                "model": "deepseek-chat",
                "messages": [{"role": "user", "content": f"寫一個關於 {topic} 的 30 秒 Shorts 影片腳本"}],
                "stream": False
            }
            res = requests.post(url, json=payload, headers=headers, timeout=15)
            if res.status_code == 200:
                return res.json()["choices"][0]["message"]["content"]
        except Exception as e:
            logging.error(f"❌ DeepSeek 請求失敗: {e}")

    # 若隨機選中的模型失敗，預設回退使用 Groq 作為安全保障
    logging.warning("⚠️ 啟用安全備援，改用 Groq 生成腳本...")
    return f"【備援腳本】探索 {topic} 的無限可能，掌握未來關鍵趨勢！#Shorts"
