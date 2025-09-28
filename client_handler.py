
import socket
import threading

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
        with self.server.condition:
            # This loop handles both initial connection and promotion from the waiting queue.
            while len(self.server.active_clients) >= self.server.max_clients:
                # If this is the first time we're checking, add to the queue.
                if self not in self.server.waiting_queue:
                    self.server.waiting_queue.append(self)
                    self.client_socket.send(f"Chat room is full. You are in the waiting queue (Position: {len(self.server.waiting_queue)}).\n".encode('utf-8'))
                    print(f"[*] Client {self.client_address} added to waiting queue.")
                
                # Wait until notified that a spot may be free.
                self.server.condition.wait()

            # If we were in the waiting queue, remove ourselves now that we are being promoted.
            if self in self.server.waiting_queue:
                self.server.waiting_queue.remove(self)
                self.client_socket.send("[PROMOTED] You are now connected to the chat.\n".encode('utf-8'))

            self._activate_and_welcome()

        try:
            while True:
                if not self.is_active: # Should only happen if client in queue disconnects
                    break

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

    def _activate_and_welcome(self):
        """Activates the client and sends a welcome message. Must be called within the condition lock."""
        self.is_active = True
        self.server.active_clients.append(self)
        print(f"[*] Client {self.client_address} joined the chat. Active clients: {len(self.server.active_clients)}")
