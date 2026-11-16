@echo off
chcp 65001 > nul
echo =================================================================
echo   ĐANG KHỞI ĐỘNG HỆ THỐNG HỖ TRỢ DỰ GIỜ - TỔ TOÁN THCS PHAN VĂN TRỊ
echo =================================================================
python server.py
if %ERRORLEVEL% NEQ 0 (
    echo Không tìm thấy Python, đang mở trực tiếp file index.html trong trình duyệt...
    start index.html
)
pause
