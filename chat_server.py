
import socket
import threading
from client_handler import ClientHandler

class ChatServer:
    """
    A multi-threaded chat server using Python's standard socket and threading libraries.
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
        # A Condition object has its own Lock, which can be used with a 'with' statement
        self.condition = threading.Condition()

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
