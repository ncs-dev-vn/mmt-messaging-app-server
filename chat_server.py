
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
        self.lock = threading.Lock()

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
        with self.lock:
            for client in self.active_clients:
                if client is not source_client:
                    try:
                        client.client_socket.send(message.encode('utf-8'))
                    except socket.error:
                        # Handle broken pipe, remove client
                        self._remove_client(client)

    def _remove_client(self, client_handler):
        """Removes a client from the active or waiting list."""
        with self.lock:
            if client_handler in self.active_clients:
                self.active_clients.remove(client_handler)
                print(f"[*] Client {client_handler.client_address} disconnected. Active clients: {len(self.active_clients)}")
                self._promote_from_waiting_queue()
            elif client_handler in self.waiting_queue:
                self.waiting_queue.remove(client_handler)
                print(f"[*] Client {client_handler.client_address} removed from waiting queue.")
            client_handler.client_socket.close()

    def _promote_from_waiting_queue(self):
        """
        Promotes the next available and connected client from the waiting queue.
        """
        while self.waiting_queue:
            next_client = self.waiting_queue.pop(0)
            try:
                # Ping the client to see if they are still connected
                next_client.client_socket.send(b'\n')
                # If the send is successful, promote them
                self.active_clients.append(next_client)
                next_client.is_active = True
                print(f"[*] Client {next_client.client_address} promoted from waiting queue. Active clients: {len(self.active_clients)}")
                next_client.client_socket.send("[PROMOTED] You are now connected to the chat.\n".encode('utf-8'))
                # Found a live client, break the loop
                break
            except socket.error:
                # If the send fails, the client is disconnected
                print(f"[*] Client {next_client.client_address} from waiting queue is disconnected. Removing.")
                next_client.client_socket.close()
                # Continue to the next client in the queue

