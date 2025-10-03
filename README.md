# Multi-User Chat Application 💬

Ứng dụng chat đa người dùng được xây dựng bằng Python với kiến trúc client-server. Đơn giản, nhanh chọn và dễ sử dụng!

## ✨ Tính năng

- **🔗 Kết nối đồng thời:** Xử lý nhiều client cùng lúc với hiệu suất cao
- **🛡️ Ổn định kết nối:** Chống chịu tốt với việc mất kết nối mạng
- **📢 Thông báo người dùng:** Broadcast thông báo khi có người tham gia/rời khỏi
- **⚡ Thời gian thực:** Chat real-time không độ trễ
- **🎯 Dễ sử dụng:** Giao diện đơn giản, không cần cài đặt phức tạp

## 🛠️ Công nghệ

- **Ngôn ngữ:** Python 3.6+
- **Thư viện:** socket, threading (built-in)
- **Kiến trúc:** Client-Server với multi-threading

## 🚀 Hướng dẫn sử dụng nhanh

### Cho người dùng thông thường

#### 1️⃣ Khởi động Server
```bash
# Mở Terminal và chạy
python3 server.py
```
Thấy thông báo này là thành công:
```
[*] Server started on 127.0.0.1:12345, waiting for connections...
```

#### 2️⃣ Tham gia Chat (mỗi người cần 1 Terminal riêng)
```bash
# Mở Terminal MỚI
python3 client.py
```
Nhập nickname khi được hỏi:
```
Đã kết nối thành công với Server.
Nhập nickname của bạn: YourName
```

#### 3️⃣ Bắt đầu Chat! 
- Gõ tin nhắn → Enter để gửi
- Gõ `quit` để thoát
- `Ctrl+C` để thoát nhanh

## 📱 Ví dụ thực tế

### Kịch bản: 3 bạn Alice, Bob, Charlie muốn chat

**Alice (làm host):**
```bash
# Alice chạy server
python3 server.py  

# Sau đó Alice mở terminal khác để chat
python3 client.py
Nickname: Alice
```

**Bob và Charlie:**
```bash
# Bob chạy client  
python3 client.py
Nickname: Bob

# Charlie chạy client
python3 client.py  
Nickname: Charlie
```

**Cuộc trò chuyện:**
```
Alice: Chào mọi người! 
Bob: Hi Alice!
Charlie: Hello cả nhà!
Alice: Hôm nay làm gì vậy?
Bob: Đi xem phim không? 
Charlie: OK luôn!
```

## 🌐 Chat qua mạng Internet/LAN

### Nếu muốn bạn bè ở xa tham gia:

#### Host (người tạo phòng):
1. Tìm IP của mình:
   ```bash
   # Windows: 
   ipconfig
   
   # Mac/Linux:
   ifconfig
   ```

2. Sửa `main.py`:
   ```python
   chat_server = ChatServer(host='0.0.0.0', port=12345)
   ```

3. Mở port 12345 trên router/firewall

#### Bạn bè (người tham gia):
Sửa `chat_client.py` hoặc tạo file mới:
```python
client = ChatClient(host='IP_CUA_HOST', port=12345)
```

## ⚙️ Tùy chỉnh

### Thay đổi số người tối đa:
```python
# Trong main.py
chat_server = ChatServer(max_clients=10)  # Cho phép 10 người
```

### Đổi cổng mạng:
```python  
# Nếu port 12345 bị chiếm dụng
ChatServer(port=8080)      # Server
ChatClient(port=8080)      # Client
```

## 🐛 Xử lý lỗi thường gặp

| Lỗi | Nguyên nhân | Giải pháp |
|-----|-------------|-----------|
| `Address already in use` | Port bị chiếm | Đợi 30s hoặc đổi port |
| `Connection refused` | Server chưa chạy | Kiểm tra server đã start chưa |
| `command not found: python3` | Python chưa cài | Thử `python` thay vì `python3` |
| Chat bị lag | Mạng yếu | Kiểm tra kết nối internet |

## 📦 Cài đặt từ đầu

### Cho người dùng thông thường (không cần code):
```bash
# Tải file release (executable) từ GitHub Releases
# Giải nén và chạy ChatServer.exe / ChatClient.exe
# Xem file HOW_TO_USE.txt để biết cách dùng
```

### Cho developer:
```bash
# 1. Clone dự án
git clone https://github.com/ncs-dev-vn/mmt-messaging-app-server.git
cd mmt-messaging-app-server

# 2. Tạo môi trường ảo (tùy chọn)
python3 -m venv venv
source venv/bin/activate  # Mac/Linux
# venv\Scripts\activate   # Windows

# 3. Chạy thử
python3 server.py
```

## 🏗️ Tạo Executable cho người dùng cuối

### Build executable files:
```bash
# Cài đặt PyInstaller
pip install pyinstaller

# Build tự động
python tools/build.py

# Kết quả trong folder release/
# - ChatServer.exe (hoặc ChatServer)  
# - ChatClient.exe (hoặc ChatClient)
# - HOW_TO_USE.txt
```

### Phân phối cho user:
1. Nén folder `release/` thành ZIP
2. Người dùng tải về, giải nén 
3. Chạy file `.exe` - không cần Python!

## 📋 Cấu trúc dự án

```
mmt-messaging-app-server/
├── 🚀 server.py              # Quick server launcher
├── 💬 client.py              # Quick client launcher
├── 📋 requirements.txt       # Dependencies
├── 📄 README.md             # This guide
│
├── 📦 src/                   # Core application code
│   ├── main.py              # Server entry point
│   ├── chat_server.py       # Server implementation  
│   ├── client_handler.py    # Client handling
│   └── chat_client.py       # Client implementation
│
├── 🔧 tools/                 # Development tools
│   ├── build.py             # Build executables
│   └── test_*.py            # Testing tools
│
├── � docs/                  # Documentation
│   ├── project_description.md
│   └── BUILD_GUIDE.md
│
├── � examples/              # Demo files
└── 🛠️ scripts/              # Utility scripts
```

## 🤝 Đóng góp

Muốn cải thiện dự án? Tạo Pull Request hoặc Issue trên GitHub!

## 📄 License

MIT License - Sử dụng tự do cho mọi mục đích.

---

**🎉 Chúc bạn có những cuộc trò chuyện vui vẻ!**

*Có thể gặp lỗi? Đọc phần "Xử lý lỗi" ở trên hoặc tạo issue trên GitHub.*
