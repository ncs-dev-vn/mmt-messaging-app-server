# Xây dựng ứng dụng Chat đa người dùng

(Multi-user Chat Application)

**Thời gian:** 5 tuần

## Mục tiêu
- Hiểu và triển khai mô hình client-server.
- Sử dụng thư viện socket và threading của Python.
- Xử lý đồng thời nhiều kết nối từ client.
- Xây dựng giao thức giao tiếp đơn giản giữa client và server.

## Gợi ý hướng dẫn

### 1. Xây dựng Server cơ bản
- **Nhiệm vụ:** Viết mã cho server. Server có khả năng chấp nhận các kết nối TCP từ nhiều client. Sử dụng thư viện threading để mỗi client kết nối sẽ được xử lý trong một luồng riêng.
- **Kết quả cần đạt:** Server có thể lắng nghe và chấp nhận nhiều kết nối client cùng lúc.

### 2. Xây dựng Client và giao tiếp cơ bản
- **Nhiệm vụ:** Viết mã cho client. Client có thể kết nối đến server, cho phép người dùng nhập tên (nickname) và gửi tin nhắn. Server nhận tin nhắn từ một client và phát lại (broadcast) cho tất cả các client khác.
- **Kết quả cần đạt:** Các client có thể gửi và nhận tin nhắn qua lại với nhau thông qua server.

### 3. Bổ sung các tính năng
- Thông báo khi một người dùng tham gia hoặc rời khỏi phòng chat.
- Xử lý việc client ngắt kết nối đột ngột.
- Hiển thị danh sách những người dùng đang online.
- Thêm tính năng gửi tin nhắn riêng tư (private message) cho một người dùng cụ thể (ví dụ: @username message).
- **Kết quả cần đạt:** Ứng dụng chat đầy đủ tính năng cơ bản và hoạt động ổn định.

---

## Lưu ý
- Dọn dẹp mã nguồn, thêm chú thích, kiểm tra và sửa lỗi.
- Viết tài liệu báo cáo đồ án, giải thích kiến trúc, các quyết định thiết kế và hướng dẫn sử dụng.
- **Kết quả cần đạt:** Mã nguồn hoàn chỉnh, sạch sẽ và một bản báo cáo chi tiết.

---

## Thư viện Python chính
- **socket:** Cho giao tiếp mạng cấp thấp.
- **threading:** Để xử lý nhiều client đồng thời.

## Cấu trúc dự án

```
mmt-messaging-app-server/
├── main.py              # Entry point của server
├── chat_server.py       # Logic chính của server
├── client_handler.py    # Xử lý từng client riêng biệt
├── chat_client.py       # Client application
├── requirements.txt     # Dependencies (nếu có)
├── project_description.md # Mô tả dự án
└── README.md           # Hướng dẫn sử dụng
```

## Các tính năng đã implement

### ✅ Đã hoàn thành:
- [x] Server cơ bản với multi-threading
- [x] Client kết nối và gửi/nhận tin nhắn
- [x] Broadcast tin nhắn cho tất cả client
- [x] Xử lý queue chờ khi server đầy
- [x] Refactor client sang OOP structure

### 🔄 Đang phát triển:
- [ ] Thông báo join/leave
- [ ] Hiển thị danh sách user online
- [ ] Private messaging
- [ ] Xử lý nickname properly
- [ ] Enhanced error handling

### 📋 Kế hoạch:
- [ ] GUI interface (optional)
- [ ] Message history
- [ ] File transfer (advanced)
- [ ] Authentication system (advanced)