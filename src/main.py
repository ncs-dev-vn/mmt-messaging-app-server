
try:
    from .chat_server import ChatServer
except ImportError:
    # For standalone testing  
    from chat_server import ChatServer
import sys
import socket

def get_local_ip():
    """Get the local IP address of this machine."""
    try:
        # Create a socket to connect to a remote address (doesn't actually connect)
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except:
        return "Unable to determine"

def main():
    """
    Initializes and starts the chat server with flexible configuration.
    """
    print("=== Multi-User Chat Server ===")
    print()
    
    # Choose server mode
    print("Server modes:")
    print("1. Local only (127.0.0.1) - Same computer only")
    print("2. Network (0.0.0.0) - Allow remote connections") 
    print("3. Quick start - Network mode")
    
    try:
        choice = input("\nChoose mode (1-3, default=3): ").strip() or "3"
        
        if choice == "1":
            host = "127.0.0.1"
            print(f"🏠 LOCAL mode: Only clients on this computer can connect")
        elif choice == "2" or choice == "3":
            host = "0.0.0.0"
            local_ip = get_local_ip()
            print(f"🌐 NETWORK mode: Clients from other computers can connect")
            print(f"📋 Your server IP address: {local_ip}")
            print(f"📝 Share this IP with friends: {local_ip}")
        else:
            print("❌ Invalid choice, using network mode")
            host = "0.0.0.0"
            
        # Port configuration
        port_input = input("Port (default=12345): ").strip()
        port = int(port_input) if port_input else 12345
        
        # Max clients
        max_input = input("Max clients (default=5): ").strip()  
        max_clients = int(max_input) if max_input else 5
        
        print(f"\n🚀 Starting server on {host}:{port}")
        print(f"👥 Maximum {max_clients} clients")
        print("🛑 Press Ctrl+C to stop")
        print("=" * 50)
        
        # Create and start server
        chat_server = ChatServer(
            host=host,
            port=port,
            max_clients=max_clients
        )
        chat_server.start()
        
    except KeyboardInterrupt:
        print("\n👋 Server shutting down...")
        sys.exit(0)
    except ValueError:
        print("❌ Invalid number input")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Server error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
