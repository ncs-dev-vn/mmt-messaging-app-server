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
        """Logic chính để xử lý kết nối khách hàng."""
        # Đầu tiên, xử lý đăng ký tên người dùng
        if not self._register_username():
            self.client_socket.close()
            return
        
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
                print(f"[*] Tin nhắn từ {self.username}: {message.strip()}")
                broadcast_message = f"{self.username}: {message}"
                self.server.broadcast(broadcast_message, self)

        except (socket.error, ConnectionResetError):
            pass # Khách hàng ngắt kết nối đột ngột
        finally:
            self.server._remove_client(self)

    def _activate_and_welcome(self):
        """Kích hoạt khách hàng và gửi tin nhắn chào mừng. Phải được gọi trong khóa điều kiện."""
        self.is_active = True
        self.server.active_clients.append(self)
        
        # Phát sóng thông báo người dùng tham gia
        join_message = f"*** {self.username} đã tham gia chat ***\n"
        self.server.broadcast(join_message, self)
        
        print(f"[*] Người dùng '{self.username}' đã tham gia chat. Khách hàng hoạt động: {len(self.server.active_clients)}")

    def _register_username(self):
        """Xử lý quá trình đăng ký tên người dùng."""
        try:
            # Gửi lời chào và yêu cầu tên người dùng
            self.client_socket.send("=== Chào mừng đến MMT Chat Server ===\n".encode('utf-8'))
            self.client_socket.send("Vui lòng nhập tên người dùng của bạn: ".encode('utf-8'))
            
            attempts = 0
            max_attempts = 3
            
            while attempts < max_attempts:
                username = self.client_socket.recv(self.server.buffer_size).decode('utf-8').strip()
                
                if not username:
                    self.client_socket.send("Tên người dùng không thể để trống. Thử lại: ".encode('utf-8'))
                    attempts += 1
                    continue
                
                # Kiểm tra xem tên người dùng đã được sử dụng chưa
                if self.server.is_username_taken(username):
                    self.client_socket.send(f"Tên người dùng '{username}' đã được sử dụng. Thử một tên khác: ".encode('utf-8'))
                    attempts += 1
                    continue
                
                # Xác thực định dạng tên người dùng
                if not self._is_valid_username(username):
                    self.client_socket.send("Định dạng tên người dùng không hợp lệ. Chỉ sử dụng chữ cái, số và dấu gạch dưới (3-20 ký tự): ".encode('utf-8'))
                    attempts += 1
                    continue
                
                # Tên người dùng hợp lệ và có sẵn
                self.username = username
                self.is_authenticated = True
                self.server.register_username(username, self)
                self.client_socket.send(f"Chào mừng, {username}!\n".encode('utf-8'))
                print(f"[*] Người dùng '{username}' đã đăng ký từ {self.client_address}")
                return True
            
            # Đã đạt số lần thử tối đa
            self.client_socket.send("Quá nhiều lần thử không thành công. Kết nối đã đóng.\n".encode('utf-8'))
            return False
            
        except socket.error:
            return False

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
            new_username = command[6:].strip()
            self._change_username(new_username)
        elif command == '/help':
            help_text = """Các lệnh có sẵn:
/users - Liệt kê tất cả người dùng đang hoạt động
/nick <tên_mới> - Thay đổi tên người dùng của bạn
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
            self.client_socket.send("Định dạng tên người dùng không hợp lệ.\n".encode('utf-8'))
            return
        
        if self.server.is_username_taken(new_username):
            self.client_socket.send("Tên người dùng đã được sử dụng.\n".encode('utf-8'))
            return
        
        old_username = self.username
        self.server.unregister_username(old_username)
        self.username = new_username
        self.server.register_username(new_username, self)
        
        self.client_socket.send(f"Tên người dùng đã được thay đổi thành '{new_username}'\n".encode('utf-8'))
        self.server.broadcast(f"*** {old_username} giờ được biết đến với tên {new_username} ***\n", self)