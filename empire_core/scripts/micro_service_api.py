try:
    from fastapi import FastAPI
    import uvicorn
except ImportError:
    import os
    os.system("pip install fastapi uvicorn > /dev/null 2>&1")
    from fastapi import FastAPI
    import uvicorn

app = FastAPI()

@app.get("/")
def home():
    return {"status": "Empire Micro-Service Online", "message": "歡迎使用陛下授權的自動化外包服務 API！"}

@app.get("/task/scrape")
def run_task(target: str = "default_target"):
    return {"result": "success", "target": target, "revenue_generated": 50}

if __name__ == "__main__":
    print("[-] [微型服務署] API 接案伺服器正在啟動...")
    uvicorn.run(app, host="127.0.0.1", port=8080)

