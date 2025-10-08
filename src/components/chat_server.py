import socket
import threading
from .client_handler import ClientHandler

class ChatServer:
    """
    Máy chủ chat hỗ trợ xử lý đa luồng sử dụng thư viện socket và threading của Python.
    """
    def __init__(self, host='127.0.0.1', port=12345, max_clients=2, buffer_size=1024):
        self.host = host
        self.port = port
        self.max_clients = max_clients
        self.buffer_size = buffer_size
        
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.active_clients = []
        self.waiting_queue = []
        self.condition = threading.Condition()

        # Quản lý tên người dùng
        self.username_registry = {}
        self.username_lock = threading.Lock()

    def start(self):
        try:
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen()
            print(f"[*] Máy chủ đã khởi động tại socket: {self.host}:{self.port}, đang lắng nghe kết nối...")
            self._accept_connections()
        except OSError as e:
            print(f"[!] Lỗi khởi động máy chủ: {e}")
        finally:
            self.server_socket.close()

    def _accept_connections(self):
        """Chấp nhận kết nối từ client mới và tạo luồng xử lý cho mỗi kết nối."""
        while True:
            try:
                client_socket, client_address = self.server_socket.accept()
                print(f"[*] Kết nối mới từ địa chỉ: {client_address[0]}:{client_address[1]}")
                handler = ClientHandler(client_socket, client_address, self)
                handler.start()
            except KeyboardInterrupt:
                print("\n[*] Máy chủ đang tắt.")
                break
            except Exception as e:
                print(f"[!] Lỗi chấp nhận kết nối: {e}")

    def broadcast(self, message, source_client=None):
        """Gửi tin nhắn đến tất cả client đang hoạt động."""
        with self.condition:
            for client in self.active_clients:
                if client is not source_client:
                    try:
                        client.client_socket.send(message.encode('utf-8'))
                    except socket.error:
                        # Xử lý kết nối bị ngắt, xoá khỏi danh sách đang hoạt động
                        self._remove_client(client)

    def register_username(self, username, client_handler):
        """Đăng ký tên người dùng cho client."""
        with self.username_lock:
            self.username_registry[username] = client_handler

    def unregister_username(self, username):
        """Hủy đăng ký tên người dùng."""
        with self.username_lock:
            self.username_registry.pop(username, None)

    def is_username_taken(self, username):
        """Kiểm tra xem tên người dùng đã tồn tại hay chưa."""
        with self.username_lock:
            return username in self.username_registry

    def get_active_users(self):
        """Lấy danh sách tên người dùng đang hoạt động."""
        with self.username_lock:
            return [username for username, handler in self.username_registry.items() 
                   if handler.is_active]

    def send_private_message(self, target_username, message, source_client):
        """Gửi tin nhắn riêng đến người dùng nào đó."""
        with self.username_lock:
            target_handler = self.username_registry.get(target_username)
            
        if target_handler and target_handler.is_active:
            try:
                # Gửi tin nhắn đến người nhận
                private_msg = f"[CÁ NHÂN] {source_client.username} -> {target_username}: {message}"
                target_handler.client_socket.send(private_msg.encode('utf-8'))

                # Gửi tin nhắn xác nhận đến người gửi
                confirmation = f"[CÁ NHÂN] Bạn -> {target_username}: {message}"
                source_client.client_socket.send(confirmation.encode('utf-8'))
                
                print(f"[*] Tin nhắn riêng từ {source_client.username} đến {target_username}: {message.strip()}")
                return True
            except socket.error:
                # Người dùng đích đã ngắt kết nối, xóa khỏi danh sách
                self._remove_client(target_handler)
                print(f"[!] Người dùng '{target_username}' đã ngắt kết nối.")
                return False
        
        return False

    def get_user_handler(self, username):
        """Tìm luồng xử lý người dùng theo tên."""
        with self.username_lock:
            return self.username_registry.get(username)

    def _remove_client(self, client_handler):
        """Xoá client khỏi danh sách đang hoạt động hoặc chờ."""
        with self.condition:
            if client_handler in self.active_clients:
                self.active_clients.remove(client_handler)
                
                # Thông báo những người dùng khác biết ai đã rời đi
                if client_handler.username:
                    leave_message = f"*** {client_handler.username} đã rời khỏi phòng chat ***\n"
                    self.broadcast(leave_message, client_handler)
                    self.unregister_username(client_handler.username)

                print(f"[*] Người dùng '{client_handler.username}' đã ngắt kết nối. Số lượng người dùng đang hoạt động: {len(self.active_clients)}")
                # Một slot đã mở. Thông báo cho luồng xử lý đang chờ để kết nối.
                self.condition.notify()
                
            elif client_handler in self.waiting_queue:
                self.waiting_queue.remove(client_handler)
                if client_handler.username:
                    self.unregister_username(client_handler.username)
                print(f"[*] Người dùng '{client_handler.username}' đã bị xóa khỏi hàng đợi chờ.")

            client_handler.client_socket.close()