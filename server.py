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
    "session": {
        "id": "TOAN8-T56-2025",
        "teacherName": "Nguyễn Thị Lan",
        "subject": "Toán",
        "className": "8A1",
        "period": "Tiết 56 (Tuần 28)",
        "teachingTime": "27/03/2025 - 08:00",
        "lessonTitle": "Bài 1. Phép thử nghiệm – Sự kiện (Chương 9)",
        "school": "THCS Phan Văn Trị",
        "district": "Phòng Giáo Dục Và Đào Tạo Gò Vấp",
        "activities": [
            {
                "id": "act-1",
                "title": "Hoạt động 1: Khởi động (Trò chơi xúc xắc & bốc thăm)",
                "time": "5 phút",
                "content": "Giáo viên tổ chức trò chơi dự đoán số chấm xúc xắc nhằm kích thích sự tò mò của học sinh về kết quả không thể đoán trước."
            },
            {
                "id": "act-2",
                "title": "Hoạt động 2: Hình thành kiến thức (Thực nghiệm 4 nhóm)",
                "time": "20 phút",
                "content": "Chia 4 nhóm: Nhóm 1 (Gieo xúc xắc), Nhóm 2 (Tung đồng xu), Nhóm 3 (Bốc thăm 1..3), Nhóm 4 (Rút bi màu). Rút ra khái niệm phép thử nghiệm và tập hợp kết quả X."
            },
            {
                "id": "act-3",
                "title": "Hoạt động 3: Luyện tập (Bài 1, Bài 2 SGK trang 107)",
                "time": "12 phút",
                "content": "Học sinh làm việc cá nhân xác định không gian kết quả của bút bi/bút chì, chọn ngày học bơi, và vòng quay số 0-9."
            },
            {
                "id": "act-4",
                "title": "Hoạt động 4: Vận dụng & Hướng dẫn tự học về nhà",
                "time": "5 phút",
                "content": "Hệ thống lại lý thuyết, dặn dò bài tập 3 trang 102 và chuẩn bị Tiết 2."
            }
        ],
        "isRegistered": True
    },
    "observations": [
        {
            "id": "sub-1",
            "observerName": "Trần Minh Tuấn",
            "timestamp": "22:30",
            "records": [
                {
                    "activityId": "act-1",
                    "activityTitle": "Hoạt động 1: Khởi động",
                    "behavior": "Học sinh hào hứng, theo dõi chăm chú video khởi động, nhiều em giơ tay dự đoán.",
                    "solution": "Vì tình huống thực tế và vui vẻ. Phát huy việc dùng trò chơi mở đầu."
                },
                {
                    "activityId": "act-2",
                    "activityTitle": "Hoạt động 2: Hình thành kiến thức",
                    "behavior": "Nhóm 1 và Nhóm 2 thực hành rất nhanh nhẹn, ghi chép đúng X={1..6}. Nhóm 4 rút bi còn lúng túng khi viết kí hiệu tập hợp.",
                    "solution": "Vì các em quên cách dùng dấu ngoặc nhọn {}. Giáo viên nên nhắc lại cách viết tập hợp trên bảng trước."
                },
                {
                    "activityId": "act-3",
                    "activityTitle": "Hoạt động 3: Luyện tập",
                    "behavior": "Đa số hoàn thành tốt bài 1. Ở bài 2 vòng quay, 3 em bỏ sót số 0.",
                    "solution": "Vì thói quen đếm từ 1. Giáo viên cần nhấn mạnh chữ số 0 khi chữa bài."
                }
            ]
        },
        {
            "id": "sub-2",
            "observerName": "Lê Thị Mai",
            "timestamp": "22:35",
            "records": [
                {
                    "activityId": "act-1",
                    "activityTitle": "Hoạt động 1: Khởi động",
                    "behavior": "Cả lớp sôi nổi, không khí học tập tích cực ngay từ phút đầu.",
                    "solution": "Cách vào bài tự nhiên, tạo tâm lý thoải mái cho học sinh."
                },
                {
                    "activityId": "act-2",
                    "activityTitle": "Hoạt động 2: Hình thành kiến thức",
                    "behavior": "Đại diện Nhóm 3 (bốc thăm) tự tin đứng lên báo cáo kết quả, nói to, rõ ràng.",
                    "solution": "Học sinh được tự tay bốc thăm nên rất hào hứng và nhớ lâu."
                },
                {
                    "activityId": "act-3",
                    "activityTitle": "Hoạt động 3: Luyện tập",
                    "behavior": "Học sinh tự giác làm bài tập cá nhân, một vài em bàn cuối còn nhìn bài bạn.",
                    "solution": "Giáo viên nên bao quát và di chuyển xuống cuối lớp nhiều hơn."
                }
            ]
        }
    ],
    "meetingMinutes": {
        "conclusion": "Tiết dạy thành công, giáo viên chuẩn bị bài chu đáo, học sinh được thực hành trải nghiệm trực quan. Các nhóm hoạt động sôi nổi. Cần lưu ý nhắc học sinh quy cách viết tập hợp đầy đủ các phần tử gồm cả số 0.",
        "evaluatedBy": "Tổ Trưởng Chuyên Môn - Thiều Thị Thúy Thanh"
    }
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
