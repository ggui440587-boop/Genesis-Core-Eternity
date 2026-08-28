from http.server import HTTPServer, BaseHTTPRequestHandler
import json

class SimpleAPIHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.end_headers()
        
        response_data = {
            "status": "Empire Micro-Service Online",
            "message": "歡迎使用陛下授權的輕量化自動化外包服務 API！"
        }
        self.wfile.write(json.dumps(response_data, ensure_ascii=False).encode('utf-8'))

if __name__ == "__main__":
    server_address = ('127.0.0.1', 8080)
    httpd = HTTPServer(server_address, SimpleAPIHandler)
    print("[-] [微型服務署] 輕量級 API 伺服器正在啟動於 http://127.0.0.1:8080 ...")
    httpd.serve_forever()

