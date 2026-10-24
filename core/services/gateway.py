import json
from http.server import HTTPServer, BaseHTTPRequestHandler
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from core.engine.base import AstraEngine

engine = AstraEngine()
MASTER_KEY = "boss1234"

class GatewayHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        
        try:
            data = json.loads(post_data.decode('utf-8'))
        except:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b'{"error": "Invalid JSON"}')
            return

        # เช็กรหัสผ่านของบอส
        if data.get("password") != MASTER_KEY:
            self.send_response(403)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Forbidden: Incorrect password"}).encode('utf-8'))
            return

        prompt = data.get("prompt", "")
        reply = engine.think(prompt)

        self.send_response(200)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.end_headers()
        self.wfile.write(json.dumps({"reply": reply}, ensure_ascii=False).encode('utf-8'))

    def log_message(self, format, *args):
        # Ghost Mode: ปิด Log เพื่อไม่ให้ทิ้งร่องรอย
        pass

if __name__ == '__main__':
    server = HTTPServer(('0.0.0.0', 9999), GatewayHandler)
    server.serve_forever()
