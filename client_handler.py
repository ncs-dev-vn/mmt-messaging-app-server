
import socket
import threading
import time

class ClientHandler(threading.Thread):
    """
    Handles communication for a single client in its own thread.
    """
    def __init__(self, client_socket, client_address, server):
        super().__init__()
        self.client_socket = client_socket
        self.client_address = client_address
        self.server = server
        self.is_active = False

    def run(self):
        """The main logic for handling a client connection."""
        with self.server.lock:
            if len(self.server.active_clients) < self.server.max_clients:
                self.is_active = True
                self.server.active_clients.append(self)
                self.client_socket.send(f"Welcome! You are connected. Active clients: {len(self.server.active_clients)}\n".encode('utf-8'))
                print(f"[*] Client {self.client_address} joined the chat. Active clients: {len(self.server.active_clients)}")
            else:
                self.server.waiting_queue.append(self)
                self.client_socket.send(f"Chat room is full. You are in the waiting queue (Position: {len(self.server.waiting_queue)}).\n".encode('utf-8'))
                print(f"[*] Client {self.client_address} added to waiting queue.")

        try:
            while True:
                if not self.is_active:
                    # For waiting clients, sleep a bit to prevent busy-waiting
                    time.sleep(1)
                    continue

                message = self.client_socket.recv(self.server.buffer_size).decode('utf-8')
                if not message:
                    break # Client disconnected
                
                print(f"[*] Message from {self.client_address}: {message.strip()}")
                broadcast_message = f"Client {self.client_address[1]}: {message}"
                self.server.broadcast(broadcast_message, self)

        except (socket.error, ConnectionResetError):
            pass # Client disconnected abruptly
        finally:
            self.server._remove_client(self)
