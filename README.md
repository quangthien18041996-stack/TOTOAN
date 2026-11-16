# HỆ THỐNG DỰ GIỜ THEO NGHIÊN CỨU BÀI HỌC - TỔ TOÁN
### Trường THCS Phan Văn Trị • Quận Gò Vấp, TP. Hồ Chí Minh

Ứng dụng web hỗ trợ số hóa quy trình dự giờ và sinh hoạt chuyên môn theo định hướng **Nghiên cứu bài học**, tuân thủ đúng quy định chuyên môn và biểu mẫu thực tế của trường THCS Phan Văn Trị.

---

## 🌟 3 PHÂN HỆ KHÉP KÍN (MÔ HÌNH 3 PHẦN)

### 1. PHẦN 1: DÀNH CHO GIÁO VIÊN GIẢNG DẠY
* Khai báo thông tin tiết dạy (Họ tên giáo viên, Lớp, Môn Toán, Tiết, Thời gian).
* Nạp Kế hoạch bài dạy (KHBD) để hệ thống tự động bóc tách tiến trình hoạt động.
* Bấm **"Hoàn tất đăng ký"** để tự động tạo **MÃ QR** phòng dự giờ chiếu lên máy chiếu hoặc in ra bàn dự giờ.

### 2. PHẦN 2: DÀNH CHO GIÁO VIÊN DỰ GIỜ (ĐIỀN PHIẾU CÁ NHÂN)
* 5 giáo viên (hoặc không giới hạn số lượng) dùng điện thoại quét mã QR để vào phòng.
* Nhận diện họ tên của từng giáo viên để cấp phát **Phiếu dự giờ cá nhân riêng biệt** trên thiết bị đó.
* Trình bày chuẩn 100% theo mẫu **PHIẾU QUAN SÁT HỌC SINH THEO NGHIÊN CỨU BÀI HỌC** của trường (Bảng 3 cột: *Nội dung hoạt động* | *Biểu hiện của học sinh* | *Nguyên nhân, biện pháp*).
* Hỗ trợ nhãn nhanh và công nghệ **Nói để nhập (Voice-to-Text)** bằng tiếng Việt.
* Tự động lưu bản nháp (Auto-save) trên từng điện thoại.
* Bấm **"Hoàn thành dự giờ"** để gửi phiếu về Phần 3 cho Tổ trưởng tổng hợp, kèm nút **"Xuất Word/PDF ký số"** cá nhân.

### 3. PHẦN 3: DÀNH CHO TỔ TRƯỞNG CHUYÊN MÔN / THƯ KÝ
* Theo dõi số lượng giáo viên đã hoàn thành nộp phiếu dự giờ thời gian thực.
* Bấm **"TỔNG HỢP KẾT QUẢ DỰ GIỜ"**: Hệ thống tự động gom toàn bộ quan sát của tất cả giáo viên về **1 PHIẾU TỔNG HỢP / BIÊN BẢN CỦA TỔ TOÁN**.
* Tổ chuyên môn thảo luận, ghi nhận kết luận chung sau cuộc họp.
* Xuất file Word (.doc) và in/lưu PDF chuẩn A4 để Giáo viên giảng dạy và Tổ trưởng ký số / ký tên hoàn tất hồ sơ.

---

## 🚀 HƯỚNG DẪN CÀI ĐẶT & CHẠY THỬ

### Cách 1: Chạy trực tiếp trên Web
Mở trực tiếp file `index.html` trong bất kỳ trình duyệt web nào (Chrome, Edge, Safari...).

### Cách 2: Chạy máy chủ mạng nội bộ (Dành cho toàn tổ kết nối qua Wi-Fi)
1. Nhấp đúp vào file `Chay_Ung_Dung.bat` (hoặc chạy lệnh `python server.py`).
2. Màn hình sẽ hiện địa chỉ IP nội bộ (ví dụ: `http://192.168.1.x:8080`).
3. Các giáo viên kết nối chung Wi-Fi trường có thể dùng điện thoại truy cập địa chỉ này hoặc quét mã QR.
