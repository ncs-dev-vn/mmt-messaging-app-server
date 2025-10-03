import socket
import threading
import sys

class ChatClient:
    """
    A chat client that connects to a chat server and handles messaging.
    """
    
    def __init__(self, host='127.0.0.1', port=12345, buffer_size=1024):
        """
        Initialize the ChatClient with server connection details.
        
        Args:
            host (str): Server host address
            port (int): Server port number
            buffer_size (int): Buffer size for receiving messages
        """
        self.host = host
        self.port = port
        self.buffer_size = buffer_size
        self.nickname = ""
        self.client_socket = None
        self.is_connected = False
        self.receive_thread = None
    
    def connect(self):
        """
        Connect to the chat server.
        
        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((self.host, self.port))
            self.is_connected = True
            print('Đã kết nối thành công với Server.')
            return True
        except socket.error as e:
            print(f"Lỗi: Không thể kết nối tới server. Lỗi: {e}")
            return False
    
    def set_nickname(self):
        """
        Prompt user to enter nickname and validate it.
        
        Returns:
            bool: True if nickname is valid, False otherwise
        """
        self.nickname = input("Nhập nickname của bạn: ").strip()
        if not self.nickname:
            print('Nickname không được để trống.')
            return False
        # Không gửi nickname cho server vì server không xử lý
        return True
    
    def receive_messages(self):
        """
        Continuously receive messages from the server in a separate thread.
        """
        while self.is_connected:
            try:
                data = self.client_socket.recv(self.buffer_size)
                if not data:
                    print('Bạn đã mất kết nối với Server.')
                    self.is_connected = False
                    break
                message = data.decode('utf-8')
                print(message)
            except Exception:
                if self.is_connected:
                    print('Bạn đã mất kết nối với Server.')
                    self.is_connected = False
                break
    
    def start_receiving_thread(self):
        """
        Start the message receiving thread.
        """
        self.receive_thread = threading.Thread(target=self.receive_messages)
        self.receive_thread.daemon = True
        self.receive_thread.start()
    
    def send_message(self, message):
        """
        Send a message to the server.
        
        Args:
            message (str): Message to send
            
        Returns:
            bool: True if message sent successfully, False otherwise
        """
        try:
            if message.strip():
                self.client_socket.send(message.encode('utf-8'))
                return True
            else:
                print('Không gửi tin nhắn rỗng.')
                return False
        except Exception:
            print('Không thể gửi tin nhắn. Đã mất kết nối với Server.')
            self.is_connected = False
            return False
    
    def handle_user_input(self):
        """
        Handle user input for sending messages and commands.
        """
        while self.is_connected:
            try:
                message = input('')
                if message.strip().lower() in ['quit', 'exit']:
                    print('Đang ngắt kết nối...')
                    self.disconnect()
                    break
                else:
                    self.send_message(message)
            except KeyboardInterrupt:
                print('\nĐang ngắt kết nối...')
                self.disconnect()
                break
            except Exception:
                print('Lỗi nhập liệu.')
                break
    
    def disconnect(self):
        """
        Disconnect from the server and clean up resources.
        """
        self.is_connected = False
        if self.client_socket:
            try:
                self.client_socket.close()
            except:
                pass
        sys.exit(0)
    
    def start(self):
        """
        Start the chat client - main entry point.
        """
        # Kết nối tới server
        if not self.connect():
            sys.exit(1)
        
        # Thiết lập nickname
        if not self.set_nickname():
            sys.exit(1)
        
        # Bắt đầu thread nhận tin nhắn
        self.start_receiving_thread()
        
        # Xử lý input từ người dùng
        self.handle_user_input()


if __name__ == "__main__":
    """
    Entry point of the chat client application.
    """
    client = ChatClient()
    client.start()