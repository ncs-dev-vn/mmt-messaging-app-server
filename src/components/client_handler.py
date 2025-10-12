import socket
import threading

class ClientHandler(threading.Thread):
    """
    Xử lý giao tiếp cho một client duy nhất trong luồng xử lý riêng.
    """
    def __init__(self, client_socket, client_address, server):
        super().__init__()
        self.client_socket = client_socket
        self.client_address = client_address
        self.server = server
        self.is_active = False
        self.username = None           # Tên người dùng đã đăng ký
        self.is_authenticated = False  # Trạng thái xác thực

    def run(self):
        """Logic chính để xử lý kết nối client."""
        # Sử dụng địa chỉ socket làm tên người dùng ban đầu
        self._register_initial_username()
        
        with self.server.condition:
            # Vòng lặp này xử lý kết nối ban đầu và đề cử kết nối mới từ hàng chờ.
            while len(self.server.active_clients) >= self.server.max_clients:
                # Nếu vượt quá số lượng tối đa, thêm vào hàng chờ.
                if self not in self.server.waiting_queue:
                    self.server.waiting_queue.append(self)
                    self.client_socket.send(f"Phòng chat đã đầy. Bạn đang trong hàng chờ (Vị trí: {len(self.server.waiting_queue)}).\n".encode('utf-8'))
                    print(f"[*] Người dùng {self.username} ({self.client_address}) được thêm vào hàng chờ.")
                
                # Chờ cho đến khi được thông báo có chỗ trống mới.
                self.server.condition.wait()

            # Xoá bản thân khỏi hàng chờ
            if self in self.server.waiting_queue:
                self.server.waiting_queue.remove(self)
                self.client_socket.send("[THÔNG BÁO] Bạn hiện đã kết nối với chat.\n".encode('utf-8'))

            # Bắt đầu kết nối và gửi tin nhắn chào mừng
            self._activate_and_welcome()

        try:
            while True:
                if not self.is_active: # Chỉ nên xảy ra nếu client trong hàng chờ ngắt kết nối
                    break

                message = self.client_socket.recv(self.server.buffer_size).decode('utf-8')
                if not message:
                    break # Client đã ngắt kết nối
                
                # Xử lý lệnh
                if message.startswith('/'):
                    self._handle_command(message.strip())
                    continue

                # Xử lý tin nhắn riêng tư với cú pháp @username <tin nhắn>
                if message.startswith('@'):
                    if self._handle_private_message(message.strip()):
                        continue
                
                # Gửi tin nhắn tới tất cả người dùng khác
                print(f"[*] Tin nhắn từ {message.strip()}")
                self.server.broadcast(message, self)

        except (socket.error, ConnectionResetError):
            pass  # Client ngắt kết nối đột ngột
        finally:
            self.server._remove_client(self)

    def _activate_and_welcome(self):
        """Kích hoạt client và gửi tin nhắn chào mừng. Phải được gọi trong khóa của self.server.condition."""
        self.is_active = True
        self.server.active_clients.append(self)
        
        # Phát sóng thông báo người dùng tham gia
        join_message = f"*** {self.username} đã tham gia chat ***\n"
        self.server.broadcast(join_message, self)
        
        print(f"[*] Người dùng '{self.username}' đã tham gia chat. Số client đang hoạt động: {len(self.server.active_clients)}")

    def _register_initial_username(self):
        """Đăng ký tên người dùng ban đầu sử dụng địa chỉ socket."""
        # Sử dụng địa chỉ IP và port làm tên người dùng ban đầu
        initial_username = f"{self.client_address[0]}:{self.client_address[1]}"
        
        # Nếu tên này đã được sử dụng, thêm số thứ tự
        counter = 1
        base_username = initial_username
        while self.server.is_username_taken(initial_username):
            initial_username = f"{base_username}_{counter}"
            counter += 1
        
        self.username = initial_username
        self.is_authenticated = True
        self.server.register_username(initial_username, self)
        print(f"[*] Người dùng '{initial_username}' đã kết nối từ {self.client_address}")

    def _is_valid_username(self, username):
        """
        Kiểm tra định dạng tên người dùng.
        Chỉ cho phép chữ cái, số và dấu gạch dưới, độ dài từ 3 đến 20 ký tự.
        """
        import re
        return re.match(r'^[a-zA-Z0-9_]{3,20}$', username) is not None

    def _handle_private_message(self, message):
        """Xử lý tin nhắn riêng tư với cú pháp @username."""
        try:
            # Phân tích định dạng tin nhắn @username
            if ' ' not in message:
                self.client_socket.send("Định dạng tin nhắn riêng tư không hợp lệ. Sử dụng: @username <tin nhắn>\n".encode('utf-8'))
                return True
            
            parts = message.split(' ', 1)
            target_username = parts[0][1:]  # Loại bỏ ký hiệu @
            private_message = parts[1]
            
            if not target_username:
                self.client_socket.send("Vui lòng chỉ định tên người dùng. Sử dụng: @username <tin nhắn>\n".encode('utf-8'))
                return True
            
            if target_username == self.username:
                self.client_socket.send("Bạn không thể gửi tin nhắn riêng tư cho chính mình.\n".encode('utf-8'))
                return True
            
            # Gửi tin nhắn riêng tư tới người dùng
            if self.server.send_private_message(target_username, private_message, self):
                return True
            
            self.client_socket.send(f"Người dùng '{target_username}' không tìm thấy hoặc đã offline.\n".encode('utf-8'))
            return True
                
        except Exception as e:
            self.client_socket.send("Lỗi xử lý tin nhắn riêng tư.\n".encode('utf-8'))
            print(f"[!] Lỗi xử lý tin nhắn riêng tư: {e}")
            return True

    def _handle_command(self, command):
        """Xử lý lệnh."""
        if command == '/users':
            users = self.server.get_active_users()
            user_list = "Người dùng đang hoạt động: " + ", ".join(users) + "\n"
            self.client_socket.send(user_list.encode('utf-8'))
        elif command == '/quit':
            self.client_socket.send("Tạm biệt!\n".encode('utf-8'))
            self.client_socket.close()
        elif command.startswith('/nick '):
            old_username = self.username
            new_username = command[6:].strip()
            success = self._change_username(new_username)
            if success:
                self.server.broadcast(f"*** Người dùng `{old_username}` đã đổi tên thành `{self.username}` ***\n", self)
        elif command == '/help':
            help_text = f"""Các lệnh có sẵn:
/users - Liệt kê tất cả người dùng đang hoạt động
/nick <tên_mới> - Thay đổi tên người dùng của bạn (hiện tại: {self.username})
/quit - Ngắt kết nối khỏi máy chủ
/help - Hiển thị tin nhắn trợ giúp này

Tin nhắn riêng tư:
@username <tin nhắn> - Gửi tin nhắn riêng tư đến người dùng cụ thể
"""
            self.client_socket.send(help_text.encode('utf-8'))
        else:
            self.client_socket.send("Lệnh không xác định. Gõ /help để xem các lệnh có sẵn.\n".encode('utf-8'))

    def _change_username(self, new_username):
        """Xử lý yêu cầu thay đổi tên người dùng."""
        if not self._is_valid_username(new_username):
            self.client_socket.send("NICKNAME_REJECTED:Định dạng tên người dùng không hợp lệ.\n".encode('utf-8'))
            return False
        
        if self.server.is_username_taken(new_username):
            self.client_socket.send("NICKNAME_TAKEN".encode('utf-8'))
            return False
        
        old_username = self.username
        self.server.unregister_username(old_username)
        self.username = new_username
        self.server.register_username(new_username, self)
        self.client_socket.send(f"NICKNAME_ACCEPTED".encode('utf-8'))
        return True