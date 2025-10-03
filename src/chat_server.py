
import socket
import threading
try:
    from .client_handler import ClientHandler
except ImportError:
    # For standalone testing
    from client_handler import ClientHandler

class ChatServer:
    """
    A multi-threaded chat server using Python's standard socket and threading libraries.
    
    Supports flexible configuration:
    - host: None for smart default, '127.0.0.1' for local, '0.0.0.0' for network
    - port: None for default 12345
    - max_clients: None for default 5
    - Environment variables: CHAT_SERVER_HOST, CHAT_NETWORK_MODE
    """
    def __init__(self, host=None, port=None, max_clients=None, buffer_size=1024):
        # Use flexible defaults instead of hard-coded values
        self.host = host if host is not None else self._get_default_host()
        self.port = port if port is not None else 12345
        self.max_clients = max_clients if max_clients is not None else 5  # Increased default
        self.buffer_size = buffer_size
        
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.active_clients = []
        self.waiting_queue = []
        # A Condition object has its own Lock, which can be used with a 'with' statement
        self.condition = threading.Condition()
    
    def _get_default_host(self):
        """
        Get default host based on environment or smart detection.
        Returns appropriate default for server binding.
        """
        import os
        
        # Check environment variable first
        env_host = os.getenv('CHAT_SERVER_HOST')
        if env_host:
            return env_host
        
        # Check if we want network mode by default
        network_mode = os.getenv('CHAT_NETWORK_MODE', 'false').lower()
        if network_mode in ['true', '1', 'yes', 'on']:
            return '0.0.0.0'  # Allow external connections
        
        # Default to localhost for security
        return '127.0.0.1'

    def start(self):
        """Binds the server to the address and starts listening for connections."""
        try:
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen()
            print(f"[*] Server started on {self.host}:{self.port}, waiting for connections...")
            self._accept_connections()
        except OSError as e:
            print(f"[!] Error starting server: {e}")
        finally:
            self.server_socket.close()

    def _accept_connections(self):
        """Accepts new client connections and spawns a handler thread for each."""
        while True:
            try:
                client_socket, client_address = self.server_socket.accept()
                print(f"[*] New connection from {client_address[0]}:{client_address[1]}")
                handler = ClientHandler(client_socket, client_address, self)
                handler.start()
            except KeyboardInterrupt:
                print("\n[*] Server is shutting down.")
                break
            except Exception as e:
                print(f"[!] Error accepting connections: {e}")

    def broadcast(self, message, source_client=None):
        """Broadcasts a message to all active clients."""
        with self.condition:
            for client in self.active_clients:
                if client is not source_client:
                    try:
                        client.client_socket.send(message.encode('utf-8'))
                    except socket.error:
                        # Handle broken pipe, remove client
                        self._remove_client(client)

    def _remove_client(self, client_handler):
        """Removes a client from the active or waiting list."""
        with self.condition:
            if client_handler in self.active_clients:
                self.active_clients.remove(client_handler)
                print(f"[*] Client {client_handler.client_address} disconnected. Active clients: {len(self.active_clients)}")
                # A slot has opened up. Notify one waiting thread so it can try to join.
                self.condition.notify()
            elif client_handler in self.waiting_queue:
                self.waiting_queue.remove(client_handler)
                print(f"[*] Client {client_handler.client_address} removed from waiting queue.")
            client_handler.client_socket.close()
