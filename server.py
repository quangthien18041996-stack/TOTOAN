import http.server
import socketserver
import webbrowser
import socket
import json
import os
import urllib.parse

PORT = 8080
DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "session_data.json")

# Default initial state if no data file exists
INITIAL_DATA = {
    "session": None,
    "sessions": [],
    "observations": [],
    "meetingMinutes": {}
}

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return INITIAL_DATA
    return INITIAL_DATA

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path == "/api/data":
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.end_headers()
            data = load_data()
            self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))
            return
        elif parsed.path == "/api/network-info":
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.end_headers()
            info = {
                "ip": get_local_ip(),
                "port": PORT
            }
            self.wfile.write(json.dumps(info).encode('utf-8'))
            return
        return super().do_GET()

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        content_length = int(self.headers.get('Content-Length', 0))
        post_body = self.rfile.read(content_length)

        try:
            payload = json.loads(post_body.decode('utf-8'))
        except Exception:
            payload = {}

        data = load_data()

        if parsed.path == "/api/register-session":
            # Part 1: Register teaching session & lesson plan
            data["session"] = payload
            data["session"]["isRegistered"] = True
            save_data(data)
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.end_headers()
            self.wfile.write(json.dumps({"success": True, "session": data["session"]}).encode('utf-8'))
            return

        elif parsed.path == "/api/submit-observation":
            # Part 2: Observer submits their observation sheet
            obs_entry = payload
            # Replace if already exists with same observerName or append
            existing = False
            for idx, item in enumerate(data["observations"]):
                if item.get("observerName") == obs_entry.get("observerName"):
                    data["observations"][idx] = obs_entry
                    existing = True
                    break
            if not existing:
                data["observations"].append(obs_entry)

            save_data(data)
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.end_headers()
            self.wfile.write(json.dumps({"success": True, "total": len(data["observations"])}).encode('utf-8'))
            return

        elif parsed.path == "/api/save-conclusion":
            # Part 3: Department head updates meeting conclusion
            data["meetingMinutes"] = payload
            save_data(data)
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.end_headers()
            self.wfile.write(json.dumps({"success": True}).encode('utf-8'))
            return

        elif parsed.path == "/api/reset-data":
            # Reset to initial demo
            save_data(INITIAL_DATA)
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.end_headers()
            self.wfile.write(json.dumps({"success": True}).encode('utf-8'))
            return

        self.send_response(404)
        self.end_headers()

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    if not os.path.exists(DATA_FILE):
        save_data(INITIAL_DATA)

    local_ip = get_local_ip()
    url_local = f"http://localhost:{PORT}/index.html"
    url_network = f"http://{local_ip}:{PORT}/index.html"

    print("="*65)
    print("  HỆ THỐNG DỰ GIỜ SỐ HÓA THEO NGHIÊN CỨU BÀI HỌC - TỔ TOÁN")
    print("  TRƯỜNG THCS PHAN VĂN TRỊ (MÔ HÌNH 3 PHẦN KHÉP KÍN)")
    print("="*65)
    print(f"[*] Mở trên máy tính này: {url_local}")
    print(f"[*] Quét mã QR / Mở trên điện thoại: {url_network}")
    print("="*65)

    with socketserver.TCPServer(("", PORT), CustomHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nĐã dừng máy chủ.")
