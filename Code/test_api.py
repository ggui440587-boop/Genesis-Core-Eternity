import requests

# 針對先前有問題或需要修正端點的金鑰進行更新測試
fix_tests = {
    "st (OpenAI 相容)": {
        "url": "https://api.openai.com/v1/models",
        "headers": {"Authorization": "Bearer AQ.Ab8RN6JHWgevS2mNoMLt7MDs6NmlL4nkrWwaLry34t9_M4C7Rg"}
    },
    "xi (xAI)": {
        "url": "https://api.x.ai/v1/models",
        "headers": {"Authorization": "Bearer xai-M5BNgXq6wCOVpNeV9bXmNqmD6CuPA80P2I1SDZXQQwqdmMOk1YNSKJX8OfHLmpOUyvEbBEIOeIwqtF5w"}
    },
    "Qwen": {
        "url": "https://dashscope.aliyuncs.com/compatible-mode/v1/models",
        "headers": {"Authorization": "Bearer sk-ws-H.DMYMYEL.ZBxw.MEUCIQCTFhmPzIFOYpsVYB5rN1sWZaVNaYKUh7Qc6pUTxrIUpgIgWy_WkOhxbUMY2zWyWuOscxfNBLn_yZi-B9c4wcXVLHQ"}
    },
    "Runlay (Runway)": {
        "url": "https://api.runwayml.com/v1/models",
        "headers": {"Authorization": "Bearer key_43c6349bdfec473196c59ad55cd109b2ea9ba39c9836123be6b08538d3a0c33a9166c5c0702a251602f64c16605980642b31ea07062cc1d2b0ec663c8b34c54a"}
    },
    "Gem (Google Gemini)": {
        "url": "https://generativelanguage.googleapis.com/v1beta/models?key=AQ.Ab8RN6JOliVUP_vhxjatYWIraxRUtDqEy4mnWeS-CjEfii4ynA",
        "headers": {}
    },
    "kIik (Kling)": {
        "url": "https://api.klingai.com/v1/v1/models", 
        "headers": {"Authorization": "Bearer api-key-kling-H1C8UYZ1_yShxFVTv9K2t83XjGT6oWIp3lDbtMIBncI"}
    },
    "Luma": {
        "url": "https://api.lumalabs.ai/dream_machine/v1/generations",
        "headers": {"Authorization": "Bearer luma-api-0SdY2t3swF2Dq5liinfAHNwarvmBG1VTXXYHB4dTXPg"}
    },
    "api": {
        "url": "https://api.openai.com/v1/models",
        "headers": {"Authorization": "Bearer sk-aWUr9Uc0LVKi1Rp9Uzxcz6E3GFYXmwpaN1ieRHgUTF2z3mqU"}
    },
    "Cod": {
        "url": "https://api.openai.com/v1/models",
        "headers": {"Authorization": "Bearer sk-BPrIHsk0cWycGCQ5BSo4Wyyzv4fc73UmR8s0HkWlWgHpLFvk"}
    }
}

def run_fix_tests():
    print("=== 開始進行問題金鑰詳細診斷測試 ===\n")
    for name, data in fix_tests.items():
        try:
            response = requests.get(data["url"], headers=data["headers"], timeout=10)
            if response.status_code == 200:
                print(f"[✅ 成功] {name}：金鑰有效！")
            else:
                # 印出詳細伺服器回應，協助我們判斷失敗原因
                error_msg = response.text.strip().replace('\n', ' ')[:100]
                print(f"[❌ 失敗/狀態碼 {response.status_code}] {name} -> 訊息: {error_msg}")
        except Exception as e:
            print(f"[⚠️ 錯誤] {name}：連線異常 ({e})")

if __name__ == "__main__":
    run_fix_tests()
