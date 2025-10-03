import socket
import threading
import sys

class ChatClient:
    """
    A chat client that connects to a chat server and handles messaging.
    """
    
    def __init__(self, host=None, port=None, buffer_size=1024):
        """
        Initialize the ChatClient with server connection details.
        
        Args:
            host (str): Server host address (None for auto-detection)
            port (int): Server port number (None for default 12345)
            buffer_size (int): Buffer size for receiving messages
        """
        # Use flexible defaults instead of hard-coded values
        self.host = host if host is not None else self._get_default_host()
        self.port = port if port is not None else 12345
        self.buffer_size = buffer_size
        self.nickname = ""
        self.client_socket = None
        self.is_connected = False
        self.receive_thread = None
    
    def _get_default_host(self):
        """
        Get default host based on context or user preference.
        Returns localhost for safety, but can be overridden.
        """
        import os
        
        # Check environment variable first
        env_host = os.getenv('CHAT_SERVER_HOST')
        if env_host:
            return env_host
            
        # Check for server on localhost first (most common case)
        if self._test_connection('127.0.0.1', 12345, timeout=1):
            return '127.0.0.1'
        
        # If no local server, return localhost anyway for safety
        # User will get connection error and can choose different option
        return '127.0.0.1'
    
    def _test_connection(self, host, port, timeout=2):
        """Test if a server is running at host:port"""
        try:
            test_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            test_socket.settimeout(timeout)
            result = test_socket.connect_ex((host, port))
            test_socket.close()
            return result == 0
        except:
            return False
    
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


def _scan_for_servers(timeout=2):
    """
    Scan local network for chat servers (experimental feature).
    
    Args:
        timeout (int): Timeout for each connection attempt
        
    Returns:
        str: IP address of found server, or None if not found
    """
    import socket
    import threading
    import time
    
    # Get local IP to determine network range
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        
        # Extract network prefix (e.g., 192.168.1.x)
        ip_parts = local_ip.split('.')
        network_prefix = f"{ip_parts[0]}.{ip_parts[1]}.{ip_parts[2]}"
        
        print(f"   Scanning network: {network_prefix}.1-254")
        
        found_servers = []
        
        def check_host(ip):
            try:
                test_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                test_socket.settimeout(timeout)
                result = test_socket.connect_ex((ip, 12345))
                test_socket.close()
                if result == 0:
                    found_servers.append(ip)
                    print(f"   ✅ Server found at {ip}")
            except:
                pass
        
        # Scan common IPs first (router, common static IPs)
        priority_ips = [f"{network_prefix}.1", f"{network_prefix}.100", 
                       f"{network_prefix}.101", f"{network_prefix}.10"]
        
        threads = []
        for ip in priority_ips:
            if ip != local_ip:  # Don't scan self
                thread = threading.Thread(target=check_host, args=(ip,))
                threads.append(thread)
                thread.start()
        
        # Wait for priority scan
        for thread in threads:
            thread.join()
        
        if found_servers:
            return found_servers[0]  # Return first found server
            
        return None
        
    except Exception as e:
        print(f"   ❌ Scan failed: {e}")
        return None

def main():
    """
    Main function with flexible client configuration.
    """
    print("=== Multi-User Chat Client ===")
    print()
    
    # Connection mode selection
    print("Connection options:")
    print("1. Local server (127.0.0.1) - Same computer")
    print("2. Remote server - Enter IP manually") 
    print("3. Quick connect - Smart defaults")
    print("4. Auto-scan local network (experimental)")
    
    try:
        choice = input("\nChoose option (1-4, default=3): ").strip() or "3"
        
        if choice == "1":
            # Local connection - explicit
            host = "127.0.0.1"
            port = 12345
            print(f"🏠 Connecting to LOCAL server")
            
        elif choice == "3":
            # Quick connect - smart default
            host = None  # Let class decide
            port = None  # Let class decide  
            print(f"⚡ Quick connect mode")
            
        elif choice == "2":
            # Remote connection
            while True:
                host = input("Enter server IP address: ").strip()
                if host:
                    break
                print("❌ IP address cannot be empty")
            
            port_input = input("Enter port (default=12345): ").strip()
            port = int(port_input) if port_input else 12345
            print(f"🌐 Connecting to REMOTE server at {host}:{port}")
            
        elif choice == "4":
            # Auto-scan local network
            print("🔍 Scanning for chat servers in local network...")
            host = _scan_for_servers()
            port = 12345
            if host:
                print(f"✅ Found server at {host}:{port}")
            else:
                print("❌ No servers found, falling back to localhost")
                host = "127.0.0.1"
            
        else:
            print("❌ Invalid choice, using local connection")
            host = "127.0.0.1"
            port = 12345
        
        print(f"\n🔗 Connecting to {host}:{port}...")
        print("💬 After connecting, you can start chatting!")
        print("📝 Commands: type 'quit' to exit, Ctrl+C for quick exit")
        print("=" * 50)
        
        # Create and start client
        client = ChatClient(host=host, port=port)
        client.start()
        
    except KeyboardInterrupt:
        print("\n👋 Exiting...")
        sys.exit(0)
    except ValueError:
        print("❌ Invalid port number")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        print("💡 Make sure the server is running and accessible")
        sys.exit(1)

if __name__ == "__main__":
    main()